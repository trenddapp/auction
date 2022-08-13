// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/IAuction.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelinUpgradeable/contracts/access/OwnableUpgradeable.sol";
import "@openzeppelinUpgradeable/contracts/proxy/utils/Initializable.sol";
import "@openzeppelinUpgradeable/contracts/proxy/utils/UUPSUpgradeable.sol";

error AuctionAlreadyStarted();
error BiddingNotStarted();
error BiddingPeriodEnded();
error BiddingPeriodNotEnded();
error InvalidAmount();
error InvalidTimestamp();
error highestBidderOnly();
error NftNotApproved();
error NftOwnerOnly();
error OwnerOnly(); // NotOwner
error TokenNotApproved();

contract Auction is
    IAuction,
    Initializable,
    UUPSUpgradeable,
    OwnableUpgradeable
{
    /// @notice Parameters of an auction
    struct AuctionInfo {
        address owner;
        address payToken;
        address highestBidder;
        uint256 highestBid;
        uint256 openingBid;
        uint64 startTime;
        uint64 endTime;
    }

    /// @inheritdoc IAuction
    mapping(address => mapping(uint256 => AuctionInfo))
        public
        override auctions;

    modifier isOngoing(address nftContractAddress, uint256 tokenId) {
        AuctionInfo memory auction = auctions[nftContractAddress][tokenId];

        if (block.timestamp > auction.endTime) revert BiddingPeriodEnded();

        if (block.timestamp < auction.startTime) revert BiddingNotStarted();
        _;
    }

    modifier onlySeller(address nftContractAddress, uint256 tokenId) {
        if (msg.sender != auctions[nftContractAddress][tokenId].owner)
            revert OwnerOnly();
        _;
    }

    /// @inheritdoc IAuction
    function bid(
        address nftContractAddress,
        uint256 tokenId,
        uint256 bidAmount
    ) external override isOngoing(nftContractAddress, tokenId) {
        AuctionInfo storage auction = auctions[nftContractAddress][tokenId];

        if (bidAmount <= auction.highestBid || bidAmount <= auction.openingBid)
            revert InvalidAmount();

        // ensure this contract is approved to move the token
        if (
            IERC20(auction.payToken).allowance(msg.sender, address(this)) <
            bidAmount
        ) revert TokenNotApproved();

        auction.highestBid = bidAmount;
        auction.highestBidder = msg.sender;

        emit BidMade(nftContractAddress, msg.sender, tokenId, bidAmount);
    }

    /// @inheritdoc IAuction
    function cancelAuction(address nftContractAddress, uint256 tokenId)
        external
        onlySeller(nftContractAddress, tokenId)
    {
        _reset(nftContractAddress, tokenId);

        emit AuctionCanceled(nftContractAddress, tokenId);
    }

    /// @inheritdoc IAuction
    function createAuction(
        address nftContractAddress,
        address payToken,
        uint256 tokenId,
        uint256 startPrice,
        uint64 startTimestamp,
        uint64 endTimestamp
    ) external override {
        // ensure sender is the owner of the NFT
        if (msg.sender != IERC721(nftContractAddress).ownerOf(tokenId))
            revert NftOwnerOnly();

        // ensure this contract is approved to move the NFT
        if (
            !IERC721(nftContractAddress).isApprovedForAll(
                msg.sender,
                address(this)
            )
        ) revert NftNotApproved();

        // check end time and start time
        if (startTimestamp < block.timestamp || endTimestamp < startTimestamp)
            revert InvalidTimestamp();

        // ensure an auction cannot be re-started if previously started
        if (auctions[nftContractAddress][tokenId].startTime != 0)
            revert AuctionAlreadyStarted();

        auctions[nftContractAddress][tokenId] = AuctionInfo({
            owner: msg.sender,
            payToken: payToken,
            highestBidder: address(0),
            highestBid: 0,
            openingBid: startPrice,
            startTime: startTimestamp,
            endTime: endTimestamp
        });

        emit AuctionCreated(
            nftContractAddress,
            msg.sender,
            tokenId,
            startPrice,
            startTimestamp,
            endTimestamp
        );
    }

    /// @inheritdoc IAuction
    function endAuction(address nftContractAddress, uint256 tokenId)
        external
        override
    {
        AuctionInfo memory auction = auctions[nftContractAddress][tokenId];

        if (block.timestamp < auction.endTime) revert BiddingPeriodNotEnded();

        _reset(nftContractAddress, tokenId);

        if (auction.highestBidder != address(0)) {
            IERC721(nftContractAddress).transferFrom(
                auction.owner,
                auction.highestBidder,
                tokenId
            );

            require(
                IERC20(auction.payToken).transferFrom(
                    auction.highestBidder,
                    auction.owner,
                    auction.highestBid
                )
            );
        }

        emit AuctionEnded(
            nftContractAddress,
            auction.highestBidder,
            tokenId,
            auction.highestBid
        );
    }

    // constructor
    function initialize() external initializer {
        __Ownable_init();
        __UUPSUpgradeable_init();
    }

    /// @inheritdoc IAuction
    function updateEndTime(
        address nftContractAddress,
        uint256 tokenId,
        uint64 newTimestamp
    )
        external
        override
        isOngoing(nftContractAddress, tokenId)
        onlySeller(nftContractAddress, tokenId)
    {
        AuctionInfo storage auction = auctions[nftContractAddress][tokenId];

        if (newTimestamp > auction.endTime) auction.endTime = newTimestamp;
        else revert InvalidTimestamp();

        emit EndTimeUpdated(nftContractAddress, tokenId, newTimestamp);
    }

    /// @inheritdoc IAuction
    function updateOpeningBid(
        address nftContractAddress,
        uint256 tokenId,
        uint256 newPrice
    )
        external
        override
        isOngoing(nftContractAddress, tokenId)
        onlySeller(nftContractAddress, tokenId)
    {
        auctions[nftContractAddress][tokenId].openingBid = newPrice;

        emit OpeningBidUpdated(nftContractAddress, tokenId, newPrice);
    }

    /// @inheritdoc IAuction
    function withdrawBid(address nftContractAddress, uint256 tokenId) external {
        AuctionInfo storage auction = auctions[nftContractAddress][tokenId];

        if (msg.sender != auction.highestBidder) revert highestBidderOnly();

        auction.highestBidder = address(0);
        auction.highestBid = 0;

        emit BidWithdrawn(nftContractAddress, tokenId);
    }

    function _authorizeUpgrade(address) internal override onlyOwner {}

    function _reset(address nftContractAddress, uint256 tokenId) private {
        delete auctions[nftContractAddress][tokenId];
    }
}
