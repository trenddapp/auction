import brownie
from brownie import accounts, Auction, AuctionProxy, AuctionV2, Contract, Weth
import pytest
from scripts.useful import encode_function_data, upgrade


@pytest.fixture
def deploy():
    weth = Weth.deploy({"from": accounts[0]})
    auction = Auction.deploy({"from": accounts[0]})
    encoded_initializer_function = encode_function_data()
    proxy = AuctionProxy.deploy(
        auction,
        encoded_initializer_function,
        {"from": accounts[0]}
    )
    auction_v2 = AuctionV2.deploy({"from": accounts[0]})

    auction_proxy = Contract.from_abi(
        "Proxy", proxy.address, auction_v2.abi)

    auction_proxy.initialize(weth, {"from": accounts[0]})

    return auction, auction_v2, auction_proxy, weth


def test_proxy_upgrades(deploy):
    proxy = deploy[2]

    with brownie.reverts():
        proxy.version() == 2


def test_proxy_upgrades_V2(deploy):
    auction_v2 = deploy[1]
    proxy = deploy[2]

    upgrade(accounts[0], proxy, auction_v2)

    assert proxy.version() == "V2"
