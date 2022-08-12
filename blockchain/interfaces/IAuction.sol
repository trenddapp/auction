// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title The interface for the auction contract
interface IAuction {
    /// @notice Emitted when an auction is created
    /// @param owner Auctioneer
    /// @param startPrice Opening bid
    /// @param startTime When the auction starts
    /// @param endTime When the auction ends
    event AuctionCreated(
        address nftContractAddress,
        address owner,
        uint256 tokenId,
        uint256 startPrice,
        uint64 startTime,
        uint64 endTime
    );

    /// @notice Emitted when the auction is ended
    /// @param highestBidder Takes ownership of the item
    event AuctionEnded(
        address nftContractAddress,
        address highestBidder,
        uint256 tokenId,
        uint256 highestBid
    );

    /// @notice Emitted when a bid is made
    event BidMade(
        address nftContractAddress,
        address bidder,
        uint256 tokenId,
        uint256 amount
    );

    /// @notice Emitted when the bid is withdrawn
    event BidWithdrawn(address nftContractAddress, uint256 tokenId);

    /// @notice Emitted when the auction is canceled
    event AuctionCanceled(address nftContractAddress, uint256 tokenId);

    /// @notice Emitted when end time of the auction is updated
    /// @param endTime New end time
    event EndTimeUpdated(
        address nftContractAddress,
        uint256 tokenId,
        uint64 endTime
    );

    /// @notice Emitted when opening bid of the auction is updated
    /// @param startPrice New opening bid
    event OpeningBidUpdated(
        address nftContractAddress,
        uint256 tokenId,
        uint256 startPrice
    );

    /// @notice Stores all information of all auctions
    /// @return The auction information for the NFT
    function auctions(address, uint256)
        external
        returns (
            address,
            address,
            address,
            uint256,
            uint256,
            uint64,
            uint64
        );

    /// @notice Make a bid for a specific NFT
    function bid(
        address nftContractAddress,
        uint256 tokenId,
        uint256 bidAmount
    ) external;

    /// @notice Cancels the auction
    function cancelAuction(address nftContractAddress, uint256 tokenId)
        external;

    /// @notice Creates an auction for the given NFT
    /// @param payToken Paying token
    /// @param startPrice Opening bid
    /// @param startTime When the auction starts
    /// @param endTime When the auction ends
    function createAuction(
        address nftContractAddress,
        address payToken,
        uint256 tokenId,
        uint256 startPrice,
        uint64 startTime,
        uint64 endTime
    ) external;

    /// @notice Ends the auction
    function endAuction(address nftContractAddress, uint256 tokenId) external;

    /// @notice Updates the end time of the auction
    function updateEndTime(
        address nftContractAddress,
        uint256 tokenId,
        uint64 newTimestamp
    ) external;

    /// @notice Updates the opening bid of the auction
    function updateOpeningBid(
        address nftContractAddress,
        uint256 tokenId,
        uint256 newPrice
    ) external;

    /// @notice Withdraws the highest bid
    function withdrawBid(address nftContractAddress, uint256 tokenId) external;
}
