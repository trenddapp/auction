from brownie import accounts, Auction, Nft, Token
import pytest
import time

TOKEN_ID = 18


@pytest.fixture
def create_auction(deploy_auction, nft, token):
    auction = deploy_auction
    opening_bid = 10 ** 18
    start_time = int(time.time()) + 1
    end_time = start_time + 20

    nft.setApprovalForAll(auction, True, {"from": accounts[0]})

    auction.createAuction(nft, token, TOKEN_ID, opening_bid,
                          start_time, end_time, {"from": accounts[0]})
    time.sleep(2)

    return auction, nft, token


@pytest.fixture
def deploy_auction():
    auction = Auction.deploy({"from": accounts[0]})
    auction.initialize({"from": accounts[0]})
    return auction


@pytest.fixture
def nft():
    return Nft.deploy({"from": accounts[0]})


@pytest.fixture
def token():
    return Token.deploy({"from": accounts[1]})
