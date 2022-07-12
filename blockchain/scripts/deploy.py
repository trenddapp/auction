from brownie import Auction, AuctionV2, AuctionProxy, config, Contract, network
from scripts.useful import encode_function_data, get_account

ACCOUNT = get_account()


def deploy_auction():
    auction = Auction.deploy(
        {"from": ACCOUNT},
        publish_source=True,
    )
    return auction


def deploy_auction_v2():
    auction_v2 = AuctionV2.deploy(
        {"from": ACCOUNT},
        publish_source=True,
    )
    return auction_v2


def deploy_proxy(logic):
    encoded_initializer_function = encode_function_data()
    proxy = AuctionProxy.deploy(
        logic,
        encoded_initializer_function,
        {"from": ACCOUNT},
        publish_source=True,
    )
    return proxy


def main():
    auction = deploy_auction()
    print(f"Auction deployed at {auction} !")
    auction.initialize(config["networks"][network.show_active()]["weth"])

    proxy = deploy_proxy(auction)
    print(f"Proxy deployed at {proxy} !")
    auction_proxy = Contract.from_abi(
        "Proxy", proxy.address, auction.abi)
    auction_proxy.initialize(
        config["networks"][network.show_active()]["weth"], {"from": ACCOUNT})
