import brownie
from brownie import Auction, Weth, Nft
import pytest
from scripts.useful import get_account
import time

ACCOUNT = get_account(1)
BIDDER = get_account(2)
TOKEN_ID = 18


@pytest.fixture
def deploy_auction():
    weth = Weth.deploy({"from": BIDDER})
    return Auction.deploy(weth, {"from": ACCOUNT}), weth


@pytest.fixture
def create_auction(deploy_auction, nft):
    auction = deploy_auction[0]
    weth = deploy_auction[1]
    starting_price = 10 ** 18
    starting_timestamp = int(time.time()) + 10
    ending_timestamp = starting_timestamp + 30

    nft.approve(auction, TOKEN_ID, {"from": ACCOUNT})

    auction.createAuction(nft, TOKEN_ID, starting_price,
                          starting_timestamp, ending_timestamp, {"from": ACCOUNT})

    time.sleep(10)

    return auction, nft, weth


@pytest.fixture
def nft():
    return Nft.deploy({"from": ACCOUNT})


def test_cant_create_auction_not_owner(deploy_auction, nft):
    starting_price = 10 ** 18
    starting_timestamp = int(time.time()) + 10
    ending_timestamp = starting_timestamp + 30

    with brownie.reverts("The sender doesn't own NFT!"):
        deploy_auction[0].createAuction(nft, TOKEN_ID, starting_price,
                                        starting_timestamp, ending_timestamp, {"from": BIDDER})


def test_cant_create_auction_started(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    starting_price = 10 ** 18
    starting_timestamp = int(time.time()) + 10
    ending_timestamp = starting_timestamp + 30

    with brownie.reverts("The auction already started by the owner!"):
        auction.createAuction(nft, TOKEN_ID, starting_price,
                              starting_timestamp, ending_timestamp, {"from": ACCOUNT})


def test_cant_create_auction_timestamp_false(deploy_auction, nft):
    starting_price = 10 ** 18
    starting_timestamp = int(time.time()) - 60
    ending_timestamp = starting_timestamp + 30

    with brownie.reverts("startingTimestamp must be greater than now!"):
        deploy_auction[0].createAuction(nft, TOKEN_ID, starting_price,
                                        starting_timestamp, ending_timestamp, {"from": ACCOUNT})


def test_cant_create_auction_nft_not_approved(deploy_auction, nft):
    starting_price = 10 ** 18
    starting_timestamp = int(time.time()) + 60
    ending_timestamp = starting_timestamp + 30

    with brownie.reverts("The NFT is not approved!"):
        deploy_auction[0].createAuction(nft, TOKEN_ID, starting_price,
                                        starting_timestamp, ending_timestamp, {"from": ACCOUNT})


def test_create_auction(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]

    assert auction.allAuctions(nft, TOKEN_ID)[-1] == ACCOUNT  # seller

    assert auction.allAuctions(nft, TOKEN_ID)[2] == 10 ** 18  # starting price


def test_cant_bid_ended(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    weth = create_auction[2]

    weth.approve(auction, 10 ** 19, {"from": BIDDER})

    time.sleep(30)

    with brownie.reverts("The auction is over!"):
        auction.bid(nft, TOKEN_ID, 10 ** 19, {"from": BIDDER})


def test_cant_bid_lower_amount(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    weth = create_auction[2]

    weth.approve(auction, 10 ** 18, {"from": BIDDER})

    with brownie.reverts("The amount must be greater than the starting price!"):
        auction.bid(nft, TOKEN_ID, 10 ** 17, {"from": BIDDER})


def test_cant_bid_seller(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]

    with brownie.reverts("The seller can not bid!"):
        auction.bid(nft, TOKEN_ID, 10 ** 19, {"from": ACCOUNT})


def test_cant_bid_weth_not_approve(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]

    with brownie.reverts("The amount is not approved!"):
        auction.bid(nft, TOKEN_ID, 10 ** 19, {"from": BIDDER})


def test_bid(create_auction):
    auction = create_auction[0]
    nft = create_auction[1]
    weth = create_auction[2]

    weth.approve(auction, 10 ** 19, {"from": BIDDER})

    auction.bid(nft, TOKEN_ID, 10 ** 19, {"from": BIDDER})

    assert auction.allAuctions(nft, TOKEN_ID)[3] == 10 ** 19  # highest bid

    assert auction.allAuctions(nft, TOKEN_ID)[4] == BIDDER  # highest bidder
