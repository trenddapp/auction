from brownie import Auction, config, network
from scripts.useful import get_account

ACCOUNT = get_account()


def deploy_auction():
    auction = Auction.deploy(
        config["networks"][network.show_active()]["weth"],
        {"from": ACCOUNT},
        publish_source=True,
    )
    return auction


def main():
    auction = deploy_auction()
    print(f"Auction deployed at {auction} !")
