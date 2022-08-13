import brownie
from brownie import accounts
import time

TOKEN_ID = 18
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
TOKEN_AMOUNT = 10 ** 19

AUCTION_ALREADY_STARTED = "typed error: 0x628e3883"
BIDDING_NOT_STARTED = "typed error: 0xe90fd1fe"
BIDDING_ENDED = "typed error: 0x2d7a45db"
BIDDING_NOT_ENDED = "typed error: 0xaae2b1aa"
INVALID_AMOUNT = "typed error: 0x2c5211c6"
INVALID_TIMESTAMP = "typed error: 0xb7d09497"
HIGHEST_BIDDER_ONLY = "typed error: 0xa44e975b"
NFT_NOT_APPROVED = "typed error: 0x6b2db6d0"
NFT_OWNER_ONLY = "typed error: 0xc594caea"
OWNER_ONLY = "typed error: 0x596dcdb8"
TOKEN_NOT_APPROVED = "typed error: 0x32da96a3"


def wait_till_end(auction, nft):
    start_time = auction.auctions(nft, TOKEN_ID)[5]
    end_time = auction.auctions(nft, TOKEN_ID)[6]
    wait_time = end_time - start_time + 10
    time.sleep(wait_time)


def test_cant_create_auction_not_owner(deploy_auction, nft, token):
    start_time = int(time.time()) + 10
    end_time = start_time + 35

    with brownie.reverts(NFT_OWNER_ONLY):
        deploy_auction.createAuction(nft, token, TOKEN_ID, TOKEN_AMOUNT,
                                     start_time, end_time, {"from": accounts[1]})


def test_cant_create_auction_started(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    token = create_auction[2]
    start_time = int(time.time()) + 10
    end_time = start_time + 35

    with brownie.reverts(AUCTION_ALREADY_STARTED):
        auction.createAuction(nft, token, TOKEN_ID, TOKEN_AMOUNT,
                              start_time, end_time, {"from": accounts[0]})


def test_cant_create_auction_invalid_timestamp(deploy_auction, nft, token):
    auction = deploy_auction
    start_time = int(time.time()) - 1
    end_time = int(time.time()) + 30

    nft.setApprovalForAll(auction, True, {"from": accounts[0]})

    with brownie.reverts(INVALID_TIMESTAMP):
        auction.createAuction(nft, token, TOKEN_ID, TOKEN_AMOUNT,
                              start_time, end_time, {"from": accounts[0]})

    start_time = int(time.time()) + 30
    end_time = int(time.time()) - 1

    with brownie.reverts(INVALID_TIMESTAMP):
        deploy_auction.createAuction(nft, token, TOKEN_ID, TOKEN_AMOUNT,
                                     start_time, end_time, {"from": accounts[0]})


def test_cant_create_auction_nft_not_approved(deploy_auction, nft, token):
    start_time = int(time.time()) + 60
    end_time = start_time + 35

    with brownie.reverts(NFT_NOT_APPROVED):
        deploy_auction.createAuction(nft, token, TOKEN_ID, TOKEN_AMOUNT,
                                     start_time, end_time, {"from": accounts[0]})


def test_create_auction(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    token = create_auction[2]

    assert auction.auctions(nft, TOKEN_ID)[0] == accounts[0]  # owner
    assert auction.auctions(nft, TOKEN_ID)[1] == token  # pay token
    assert auction.auctions(nft, TOKEN_ID)[2] == ZERO_ADDRESS  # highest bidder
    assert auction.auctions(nft, TOKEN_ID)[3] == 0  # highest bid
    assert auction.auctions(nft, TOKEN_ID)[4] != 0  # opening bid
    assert auction.auctions(nft, TOKEN_ID)[5] != 0  # start time
    assert auction.auctions(nft, TOKEN_ID)[6] != 0  # end time


def test_cant_bid_ended(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    token = create_auction[2]

    token.approve(auction, TOKEN_AMOUNT, {"from": accounts[1]})

    wait_till_end(auction, nft)

    with brownie.reverts(BIDDING_ENDED):
        auction.bid(nft, TOKEN_ID, TOKEN_AMOUNT, {"from": accounts[1]})


def test_cant_bid_invalid_amount(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    token = create_auction[2]

    bid_amount = 10 ** 17

    token.approve(auction, bid_amount, {"from": accounts[1]})

    with brownie.reverts(INVALID_AMOUNT):
        auction.bid(nft, TOKEN_ID, bid_amount, {"from": accounts[1]})


def test_cant_bid_token_not_approve(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]

    with brownie.reverts(TOKEN_NOT_APPROVED):
        auction.bid(nft, TOKEN_ID, TOKEN_AMOUNT, {"from": accounts[1]})


def test_bid(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    token = create_auction[2]

    token.approve(auction, TOKEN_AMOUNT, {"from": accounts[1]})

    auction.bid(nft, TOKEN_ID, TOKEN_AMOUNT, {"from": accounts[1]})

    assert auction.auctions(nft, TOKEN_ID)[2] == accounts[1]  # highest bidder

    assert auction.auctions(nft, TOKEN_ID)[3] == TOKEN_AMOUNT  # highest bid


def test_cant_update_timestamp_ended(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    new_timestamp = int(time.time()) + 10

    wait_till_end(auction, nft)

    with brownie.reverts(BIDDING_ENDED):
        auction.updateEndTime(
            nft, TOKEN_ID, new_timestamp, {"from": accounts[0]})


def test_cant_update_timestamp_not_owner(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    new_timestamp = int(time.time()) + 10

    with brownie.reverts(OWNER_ONLY):
        auction.updateEndTime(
            nft, TOKEN_ID, new_timestamp, {"from": accounts[1]})


def test_cant_update_timestamp_invalid_time(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    new_timestamp = int(time.time())

    with brownie.reverts(INVALID_TIMESTAMP):
        auction.updateEndTime(
            nft, TOKEN_ID, new_timestamp, {"from": accounts[0]})


def test_update_timestamp(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    new_timestamp = auction.auctions(nft, TOKEN_ID)[-1] + 30

    auction.updateEndTime(
        nft, TOKEN_ID, new_timestamp, {"from": accounts[0]})

    assert auction.auctions(nft, TOKEN_ID)[-1] == new_timestamp


def test_cant_update_price_ended(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    new_price = 10 ** 20

    wait_till_end(auction, nft)

    with brownie.reverts(BIDDING_ENDED):
        auction.updateOpeningBid(
            nft, TOKEN_ID, new_price, {"from": accounts[0]})


def test_cant_update_price_not_owner(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    new_price = 10 ** 20

    with brownie.reverts(OWNER_ONLY):
        auction.updateOpeningBid(
            nft, TOKEN_ID, new_price, {"from": accounts[1]})


def test_update_price(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    new_price = 10 ** 20

    auction.updateOpeningBid(
        nft, TOKEN_ID, new_price, {"from": accounts[0]})

    assert auction.auctions(nft, TOKEN_ID)[4] == new_price


def test_cant_end_ongoing(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]

    with brownie.reverts(BIDDING_NOT_ENDED):
        auction.endAuction(nft, TOKEN_ID, {"from": accounts[0]})


def test_end(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]

    wait_till_end(auction, nft)

    auction.endAuction(nft, TOKEN_ID, {"from": accounts[0]})

    assert auction.auctions(nft, TOKEN_ID)[0] == ZERO_ADDRESS  # owner
    assert auction.auctions(nft, TOKEN_ID)[1] == ZERO_ADDRESS  # pay token
    assert auction.auctions(nft, TOKEN_ID)[2] == ZERO_ADDRESS  # highest bidder
    assert auction.auctions(nft, TOKEN_ID)[3] == 0  # highest bid
    assert auction.auctions(nft, TOKEN_ID)[4] == 0  # opening bid
    assert auction.auctions(nft, TOKEN_ID)[5] == 0  # start time
    assert auction.auctions(nft, TOKEN_ID)[6] == 0  # end time
