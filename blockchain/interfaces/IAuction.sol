// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title The interface for the auction contract
interface IAuction {
    /// @notice Emitted when an auction is created
    /// @param startingPrice Opening bid
    /// @param startingTimestamp When the auction starts
    /// @param endingTimestamp When the auction ends
    /// @param seller Auctioneer
    event AuctionCreated(
        address nftContractAddress,
        uint256 tokenId,
        uint256 startingPrice,
        uint64 startingTimestamp,
        uint64 endingTimestamp,
        address seller
    );

    /// @notice Emitted when the auction is ended
    /// @param highestBidder Takes ownership of the item
    event AuctionEnded(
        address nftContractAddress,
        uint256 tokenId,
        uint256 highestBid,
        address highestBidder
    );

    /// @notice Emitted when a bid is made
    event BidMade(
        address nftContractAddress,
        uint256 tokenId,
        uint256 amount,
        address bidder
    );

    /// @notice Emitted when end time of the auction is updated
    /// @param endingTimestamp New end time
    event EndingTimestampUpdated(
        address nftContractAddress,
        uint256 tokenId,
        uint64 endingTimestamp
    );

    /// @notice Emitted when opening bid of the auction is updated
    /// @param startingPrice New opening bid
    event StartingPriceUpdated(
        address nftContractAddress,
        uint256 tokenId,
        uint256 startingPrice
    );

    /// @notice Stores all information of all auctions
    /// @return The auction information for the NFT
    function allAuctions(address _nftContractAddress, uint256 _tokenId)
        external
        returns (
            uint64,
            uint64,
            uint256,
            uint256,
            address,
            address
        );

    /// @notice Bid for a specific NFT
    function bid(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _bidAmount
    ) external;

    /// @notice Creates an auction for the given NFT
    /// @param _startingPrice Opening bid
    /// @param _startingTimestamp When the auction starts
    /// @param _endingTimestamp When the auction ends
    function createAuction(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _startingPrice,
        uint64 _startingTimestamp,
        uint64 _endingTimestamp
    ) external;

    /// @notice Ends the auction
    function endAuction(address _nftContractAddress, uint256 _tokenId) external;

    /// @notice If the auction does not end after 7 days, it will terminate the auction
    function forceReset(address _nftContractAddress, uint256 _tokenId) external;

    /// @notice Updates the end time of the auction
    function updateEndingTimestamp(
        address _nftContractAddress,
        uint256 _tokenId,
        uint64 _newEndingTimestamp
    ) external;

    /// @notice Updates the opening bid of the auction
    function updateStartingPrice(
        address _nftContractAddress,
        uint256 _tokenId,
        uint256 _newStartingPrice
    ) external;
}
