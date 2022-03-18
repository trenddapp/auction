//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract Auction {
    struct AuctionInfo {
        uint64 startingTimestamp;
        uint64 endingTimestamp;
        uint128 startingPrice;
        uint128 highestBid;
        address highestBidder;
        address seller;
    }
    mapping(address => mapping(uint256 => AuctionInfo)) public allAuctions;
    mapping(address => mapping(uint256 => mapping(address => uint256)))
        public auctionBids;

    event AuctionCreated(
        address nftContractAddress,
        uint256 tokenId,
        uint128 startingPrice,
        uint64 duration,
        address seller
    );

    event BidMade(
        address nftContractAddress,
        uint256 tokenId,
        uint256 amount,
        address bidder
    );

    event BidWithdrawn(
        address nftContractAddress,
        uint256 _tokenId,
        address bidder
    );

    event EndingTimestampUpdated(address nftContractAddress, uint256 tokenId);

    event StartingPriceUpdated(address nftContractAddress, uint256 tokenId);

    modifier auctionNotStarted(address _nftContractAddress, uint256 _tokenId) {
        require(
            allAuctions[_nftContractAddress][_tokenId].seller == address(0),
            "The auction already started by the owner"
        );
        _;
    }

    modifier onlyNftOwner(address _nftContractAddress, uint256 _tokenId) {
        require(
            msg.sender == IERC721(_nftContractAddress).ownerOf(_tokenId),
            "The sender doesn't own NFT!"
        );
        _;
    }

    modifier onlyBidder(address _nftContractAddress, uint256 _tokenId) {
        require(
            auctionBids[_nftContractAddress][_tokenId][msg.sender] > 0,
            "You did not bid any amount!"
        );
        _;
    }

    modifier onlySeller(address _nftContractAddress, uint256 _tokenId) {
        require(
            msg.sender == allAuctions[_nftContractAddress][_tokenId].seller,
            "The sender is not the seller!"
        );
        _;
    }

    modifier checkBidAmount(
        address _nftContractAddress,
        uint256 _tokenId,
        uint128 _amount
    ) {
        require(
            _amount > allAuctions[_nftContractAddress][_tokenId].highestBid,
            "The amount must be greater than the highest bid!"
        );
        require(
            _amount > allAuctions[_nftContractAddress][_tokenId].startingPrice,
            "The amount must be greater than the starting price!"
        );
        _;
    }

    modifier ifOngoing(address _nftContractAddress, uint256 _tokenId) {
        require(
            block.timestamp <
                allAuctions[_nftContractAddress][_tokenId].endingTimestamp,
            "The auction is over!"
        );
        _;
    }

    function bid(address _nftContractAddress, uint256 _tokenId)
        external
        payable
        ifOngoing(_nftContractAddress, _tokenId)
        checkBidAmount(_nftContractAddress, _tokenId, msg.value)
    {
        auctionBids[_nftContractAddress][_tokenId][msg.sender] = msg.value;
        allAuctions[_nftContractAddress][_tokenId].highestBid = msg.value;
        allAuctions[_nftContractAddress][_tokenId].highestBidder = msg.sender;

        emit BidMade(_nftContractAddress, _tokenId, msg.value, msg.sender);
    }

    function createAuction(
        address _nftContractAddress,
        uint256 _tokenId,
        uint128 _startingPrice,
        uint64 _startingTimestamp,
        uint64 _endingTimestamp
    )
        external
        onlyNftOwner(_nftContractAddress, _tokenId)
        auctionNotStarted(_nftContractAddress, _tokenId)
    {
        _nftContractAddress.transferFrom(msg.sender, address(this), _tokenId);

        allAuctions[_nftContractAddress][_tokenId] = AuctionInfo(
            _startingTimestamp,
            _endingTimestamp,
            _startingPrice,
            0, // highestBid
            address(0), // highestBidder
            msg.sender
        );

        emit AuctionCreated(
            _nftContractAddress,
            _tokenId,
            _startingPrice,
            _endingTimestamp - _startingTimestamp,
            msg.sender
        );
    }

    function withdrawBid(address _nftContractAddress, uint256 _tokenId)
        external
        onlyBidder(_nftContractAddress, _tokenId)
    {
        uint256 amount = auctionBids[_nftContractAddress][_tokenId][msg.sender];
        auctionBids[_nftContractAddress][_tokenId][msg.sender] = 0;
        _withdraw(_nftContractAddress, _tokenId, amount);

        emit BidWithdrawn(_nftContractAddress, _tokenId, msg.sender);
    }

    function updateStartingPrice(
        address _nftContractAddress,
        uint256 _tokenId,
        uint128 _newStartingPrice
    ) external onlySeller(_nftContractAddress, _tokenId) {
        allAuctions[_nftContractAddress][_tokenId]
            .startingPrice = _newStartingPrice;

        emit StartingPriceUpdated(_nftContractAddress, _tokenId);
    }

    function updateEndingTimestamp(
        address _nftContractAddress,
        uint256 _tokenId,
        uint64 _newEndingTimestamp
    ) external onlySeller(_nftContractAddress, _tokenId) {
        allAuctions[_nftContractAddress][_tokenId]
            .endingTimestamp = _newEndingTimestamp;

        emit EndingTimestampUpdated(_nftContractAddress, _tokenId);
    }

    function _withdraw(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _amount
    ) private {
        payable(msg.sender).transfer(_amount);
    }
}
