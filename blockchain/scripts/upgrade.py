from brownie import AuctionProxy
from scripts.deploy import deploy_auction_v2
from scripts.useful import get_account, upgrade


def upgrade_auction(account, proxy, new_implementation):
    upgrade(account, proxy, new_implementation)
    print("Proxy has been upgraded!")


def main():
    account = get_account()
    proxy = AuctionProxy[-1]
    auction_new_version = deploy_auction_v2()
    upgrade_auction(account, proxy, auction_new_version)
