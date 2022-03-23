// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract Auction {
    address constant WETH = 0xDf032Bc4B9dC2782Bb09352007D4C57B75160B15;

    struct AuctionInfo {
        uint64 startingTimestamp;
        uint64 endingTimestamp;
        uint256 startingPrice;
        uint256 highestBid;
        address highestBidder;
        address seller;
    }
    mapping(address => mapping(uint256 => AuctionInfo)) public allAuctions;
    mapping(address => mapping(uint256 => mapping(address => uint256)))
        public auctionBids;

    event AuctionCanceled(address nftContractAddress, uint256 tokenId);

    event AuctionCreated(
        address nftContractAddress,
        uint256 tokenId,
        uint256 startingPrice,
        uint64 startingTimestamp,
        uint64 endingTimestamp,
        address seller
    );

    event AuctionEnded(
        address nftContractAddress,
        uint256 tokenId,
        uint256 highestBid,
        address highestBidder
    );

    event BidMade(
        address nftContractAddress,
        uint256 tokenId,
        uint256 amount,
        address bidder
    );

    event BidCanceled(
        address nftContractAddress,
        uint256 _tokenId,
        address bidder
    );

    event EndingTimestampUpdated(
        address nftContractAddress,
        uint256 tokenId,
        uint64 endingTimestamp
    );

    event StartingPriceUpdated(
        address nftContractAddress,
        uint256 tokenId,
        uint256 startingPrice
    );

    modifier auctionNotStarted(address _nftContractAddress, uint256 _tokenId) {
        require(
            allAuctions[_nftContractAddress][_tokenId].seller == address(0),
            "The auction already started by the owner"
        );
        _;
    }

    modifier checkBidAmount(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _amount
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

    modifier checkTimestamp(
        uint64 _startingTimestamp,
        uint64 _endingTimestamp
    ) {
        require(
            _startingTimestamp >= block.timestamp,
            "startingTimestamp must be greater than now!"
        );
        require(
            _endingTimestamp > _startingTimestamp,
            "endingTimestamp must be greater than startingTimestamp!"
        );
        _;
    }

    modifier ifApprovedNft(address _nftContractAddress, uint256 _tokenId) {
        require(
            IERC721(_nftContractAddress).getApproved(_tokenId) == address(this),
            "The NFT is not approved!"
        );
        _;
    }

    modifier ifApprovedWeth(address _owner, uint256 _amount) {
        require(
            IERC20(WETH).allowance(_owner, address(this)) >= _amount,
            "The amount is not approved!"
        );
        _;
    }

    modifier ifEnded(address _nftContractAddress, uint256 _tokenId) {
        require(
            block.timestamp >
                allAuctions[_nftContractAddress][_tokenId].endingTimestamp,
            "The auction is not over!"
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

    modifier notSeller(
        address _nftContractAddress,
        uint256 _tokenId,
        address _sender
    ) {
        require(
            _sender != allAuctions[_nftContractAddress][_tokenId].seller,
            "The seller can not bid!"
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

    modifier onlyNftOwner(address _nftContractAddress, uint256 _tokenId) {
        require(
            msg.sender == IERC721(_nftContractAddress).ownerOf(_tokenId),
            "The sender doesn't own NFT!"
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

    function bid(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _bidAmount
    )
        external
        ifOngoing(_nftContractAddress, _tokenId)
        checkBidAmount(_nftContractAddress, _tokenId, _bidAmount)
        notSeller(_nftContractAddress, _tokenId, msg.sender)
        ifApprovedWeth(msg.sender, _bidAmount)
    {
        auctionBids[_nftContractAddress][_tokenId][msg.sender] = _bidAmount;
        allAuctions[_nftContractAddress][_tokenId].highestBid = _bidAmount;
        allAuctions[_nftContractAddress][_tokenId].highestBidder = msg.sender;

        emit BidMade(_nftContractAddress, _tokenId, _bidAmount, msg.sender);
    }

    function cancelAuction(address _nftContractAddress, uint256 _tokenId)
        external
        ifOngoing(_nftContractAddress, _tokenId)
        onlySeller(_nftContractAddress, _tokenId)
    {
        _reset(_nftContractAddress, _tokenId);

        emit AuctionCanceled(_nftContractAddress, _tokenId);
    }

    function cancelBid(address _nftContractAddress, uint256 _tokenId)
        external
        onlyBidder(_nftContractAddress, _tokenId)
    {
        auctionBids[_nftContractAddress][_tokenId][msg.sender] = 0;

        emit BidCanceled(_nftContractAddress, _tokenId, msg.sender);
    }

    function createAuction(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _startingPrice,
        uint64 _startingTimestamp,
        uint64 _endingTimestamp
    )
        external
        onlyNftOwner(_nftContractAddress, _tokenId)
        auctionNotStarted(_nftContractAddress, _tokenId)
        checkTimestamp(_startingTimestamp, _endingTimestamp)
        ifApprovedNft(_nftContractAddress, _tokenId)
    {
        allAuctions[_nftContractAddress][_tokenId] = AuctionInfo(
            _startingTimestamp,
            _endingTimestamp,
            _startingPrice,
            0,
            address(0),
            msg.sender
        );

        emit AuctionCreated(
            _nftContractAddress,
            _tokenId,
            _startingPrice,
            _startingTimestamp,
            _endingTimestamp,
            msg.sender
        );
    }

    function updateEndingTimestamp(
        address _nftContractAddress,
        uint256 _tokenId,
        uint64 _newEndingTimestamp
    )
        external
        ifOngoing(_nftContractAddress, _tokenId)
        onlySeller(_nftContractAddress, _tokenId)
    {
        allAuctions[_nftContractAddress][_tokenId]
            .endingTimestamp = _newEndingTimestamp;

        emit EndingTimestampUpdated(
            _nftContractAddress,
            _tokenId,
            _newEndingTimestamp
        );
    }

    function updateStartingPrice(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _newStartingPrice
    )
        external
        ifOngoing(_nftContractAddress, _tokenId)
        onlySeller(_nftContractAddress, _tokenId)
    {
        allAuctions[_nftContractAddress][_tokenId]
            .startingPrice = _newStartingPrice;

        emit StartingPriceUpdated(
            _nftContractAddress,
            _tokenId,
            _newStartingPrice
        );
    }

    function _reset(address _nftContractAddress, uint256 _tokenId) private {
        allAuctions[_nftContractAddress][_tokenId] = AuctionInfo(
            0,
            0,
            0,
            0,
            address(0),
            address(0)
        );
    }
}
