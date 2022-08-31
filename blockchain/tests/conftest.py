from brownie import accounts, Auction, chain, Nft, Token, Wei
import pytest
import time

TOKEN_ID = 18


def auctioneer():
    return accounts[0]


def bidder():
    return accounts[1]


@pytest.fixture
def create_auction(deploy_auction, nft, token):
    auction = deploy_auction
    opening_bid = Wei("1 ether")
    start_time = chain.time() + 1
    end_time = start_time + 20

    nft.setApprovalForAll(auction, True, {"from": auctioneer()})

    auction.createAuction(nft, token, TOKEN_ID, opening_bid,
                          start_time, end_time, {"from": auctioneer()})
    time.sleep(2)

    return auction, nft, token


@pytest.fixture
def deploy_auction():
    auction = Auction.deploy({"from": auctioneer()})
    auction.initialize({"from": auctioneer()})
    return auction


@pytest.fixture
def nft():
    return Nft.deploy({"from": auctioneer()})


@pytest.fixture
def token():
    return Token.deploy({"from": bidder()})
