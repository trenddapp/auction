import time
from web3 import Web3
from dotenv import load_dotenv
import os
load_dotenv()  # .env file

INFURA_API_KEY = os.getenv("WEB3_INFURA_PROJECT_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_KEY = "0x9Cdb45dd263327416118778b927C9050a3461c30"
INFURA_URL = f"https://rinkeby.infura.io/v3/{INFURA_API_KEY}"

# instantiate a Web3 connection
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
# this will return True if the connection is live
print(web3.isConnected())

abi = [
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "previousAdmin",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "address",
                'name': "newAdmin",
                'type': "address"
            }
        ],
        'name': "AdminChanged",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "startingPrice",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint64",
                'name': "startingTimestamp",
                'type': "uint64"
            },
            {
                'indexed': False,
                'internalType': "uint64",
                'name': "endingTimestamp",
                'type': "uint64"
            },
            {
                'indexed': False,
                'internalType': "address",
                'name': "seller",
                'type': "address"
            }
        ],
        'name': "AuctionCreated",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "highestBid",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "address",
                'name': "highestBidder",
                'type': "address"
            }
        ],
        'name': "AuctionEnded",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': True,
                'internalType': "address",
                'name': "beacon",
                'type': "address"
            }
        ],
        'name': "BeaconUpgraded",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "amount",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "address",
                'name': "bidder",
                'type': "address"
            }
        ],
        'name': "BidMade",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint64",
                'name': "endingTimestamp",
                'type': "uint64"
            }
        ],
        'name': "EndingTimestampUpdated",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': True,
                'internalType': "address",
                'name': "previousOwner",
                'type': "address"
            },
            {
                'indexed': True,
                'internalType': "address",
                'name': "newOwner",
                'type': "address"
            }
        ],
        'name': "OwnershipTransferred",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "startingPrice",
                'type': "uint256"
            }
        ],
        'name': "StartingPriceUpdated",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': True,
                'internalType': "address",
                'name': "implementation",
                'type': "address"
            }
        ],
        'name': "Upgraded",
        'type': "event"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'name': "allAuctions",
        'outputs': [
            {
                'internalType': "uint64",
                'name': "startingTimestamp",
                'type': "uint64"
            },
            {
                'internalType': "uint64",
                'name': "endingTimestamp",
                'type': "uint64"
            },
            {
                'internalType': "uint256",
                'name': "startingPrice",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "highestBid",
                'type': "uint256"
            },
            {
                'internalType': "address",
                'name': "highestBidder",
                'type': "address"
            },
            {
                'internalType': "address",
                'name': "seller",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "_bidAmount",
                'type': "uint256"
            }
        ],
        'name': "bid",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "_startingPrice",
                'type': "uint256"
            },
            {
                'internalType': "uint64",
                'name': "_startingTimestamp",
                'type': "uint64"
            },
            {
                'internalType': "uint64",
                'name': "_endingTimestamp",
                'type': "uint64"
            }
        ],
        'name': "createAuction",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            }
        ],
        'name': "endAuction",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            }
        ],
        'name': "forceReset",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_weth",
                'type': "address"
            }
        ],
        'name': "initialize",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "owner",
        'outputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "proxiableUUID",
        'outputs': [
            {
                'internalType': "bytes32",
                'name': "",
                'type': "bytes32"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "renounceOwnership",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "newOwner",
                'type': "address"
            }
        ],
        'name': "transferOwnership",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "uint64",
                'name': "_newEndingTimestamp",
                'type': "uint64"
            }
        ],
        'name': "updateEndingTimestamp",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "_newStartingPrice",
                'type': "uint256"
            }
        ],
        'name': "updateStartingPrice",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "newImplementation",
                'type': "address"
            }
        ],
        'name': "upgradeTo",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "newImplementation",
                'type': "address"
            },
            {
                'internalType': "bytes",
                'name': "data",
                'type': "bytes"
            }
        ],
        'name': "upgradeToAndCall",
        'outputs': [],
        'stateMutability': "payable",
        'type': "function"
    }
]

contract_address = "0x9080cb527B8D55f72046ad1eF52ed95bd9075BDd"
contract = web3.eth.contract(address=contract_address, abi=abi)


def upgrade():
    # 1
    nonce = web3.eth.getTransactionCount(PUBLIC_KEY)
    tx = contract.functions.upgradeTo(
        "0xCC91Bf21DA2026863C87754904f731C0b8a07c2c"
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


upgrade()
# # eval() function to evaluate Python source code
abi = [{"constant": False, "inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "approve", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}, {"constant": False, "inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "mint", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}, {"constant": False, "inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "safeTransferFrom", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}, {"constant": False, "inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "bytes", "name": "_data", "type": "bytes"}], "name": "safeTransferFrom", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}, {"constant": False, "inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "bool", "name": "approved", "type": "bool"}], "name": "setApprovalForAll", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}, {"constant": False, "inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "transferFrom", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "payable": False, "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"}, {"indexed": True, "internalType": "address", "name": "to",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Transfer", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "approved", "type": "address"}, {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "operator", "type": "address"}, {"indexed": False, "internalType": "bool", "name": "approved", "type": "bool"}], "name": "ApprovalForAll", "type": "event"}, {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"}, {"constant": True, "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "getApproved", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"}, {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "operator", "type": "address"}], "name": "isApprovedForAll", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "view", "type": "function"}, {"constant": True, "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "ownerOf", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"}, {"constant": True, "inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "payable": False, "stateMutability": "view", "type": "function"}]

contract_address = "0x94b1bd2a4ACFa531C8C330c389072Cb08Db28108"
erc721_contract = web3.eth.contract(address=contract_address, abi=abi)


def aprrove():
    # 1
    nonce = web3.eth.getTransactionCount(PUBLIC_KEY)
    tx = erc721_contract.functions.setApprovalForAll(
        "0x120810abF6a65Ee1FCb0D17b957b756d63716864",
        True
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


# aprrove()

def aprroveS():
    # 1
    nonce = web3.eth.getTransactionCount(
        PUBLIC_KEY)
    tx = erc721_contract.functions.approve(
        "0x52aFa4a1F861cAB8022bdcf053b523d9C1b75Ec2",
        70948226068845075091097172684116137139687598325071419309035027374095581839363
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


# aprroveS()

abi = [
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            }
        ],
        'name': "AuctionCanceled",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "startingPrice",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint64",
                'name': "startingTimestamp",
                'type': "uint64"
            },
            {
                'indexed': False,
                'internalType': "uint64",
                'name': "endingTimestamp",
                'type': "uint64"
            },
            {
                'indexed': False,
                'internalType': "address",
                'name': "seller",
                'type': "address"
            }
        ],
        'name': "AuctionCreated",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "highestBid",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "address",
                'name': "highestBidder",
                'type': "address"
            }
        ],
        'name': "AuctionEnded",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "address",
                'name': "bidder",
                'type': "address"
            }
        ],
        'name': "BidCanceled",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "amount",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "address",
                'name': "bidder",
                'type': "address"
            }
        ],
        'name': "BidMade",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint64",
                'name': "endingTimestamp",
                'type': "uint64"
            }
        ],
        'name': "EndingTimestampUpdated",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': False,
                'internalType': "address",
                'name': "nftContractAddress",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "tokenId",
                'type': "uint256"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "startingPrice",
                'type': "uint256"
            }
        ],
        'name': "StartingPriceUpdated",
        'type': "event"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'name': "allAuctions",
        'outputs': [
            {
                'internalType': "uint64",
                'name': "startingTimestamp",
                'type': "uint64"
            },
            {
                'internalType': "uint64",
                'name': "endingTimestamp",
                'type': "uint64"
            },
            {
                'internalType': "uint256",
                'name': "startingPrice",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "highestBid",
                'type': "uint256"
            },
            {
                'internalType': "address",
                'name': "highestBidder",
                'type': "address"
            },
            {
                'internalType': "address",
                'name': "seller",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            },
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'name': "auctionBids",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "_bidAmount",
                'type': "uint256"
            }
        ],
        'name': "bid",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            }
        ],
        'name': "cancelAuction",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            }
        ],
        'name': "cancelBid",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "_startingPrice",
                'type': "uint256"
            },
            {
                'internalType': "uint64",
                'name': "_startingTimestamp",
                'type': "uint64"
            },
            {
                'internalType': "uint64",
                'name': "_endingTimestamp",
                'type': "uint64"
            }
        ],
        'name': "createAuction",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            }
        ],
        'name': "endAuction",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_operator",
                'type': "address"
            },
            {
                'internalType': "address",
                'name': "_from",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "bytes",
                'name': "_data",
                'type': "bytes"
            }
        ],
        'name': "onERC721Received",
        'outputs': [
            {
                'internalType': "bytes4",
                'name': "",
                'type': "bytes4"
            }
        ],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "uint64",
                'name': "_newEndingTimestamp",
                'type': "uint64"
            }
        ],
        'name': "updateEndingTimestamp",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "_nftContractAddress",
                'type': "address"
            },
            {
                'internalType': "uint256",
                'name': "_tokenId",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "_newStartingPrice",
                'type': "uint256"
            }
        ],
        'name': "updateStartingPrice",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    }
]
contract_address = "0x0a983181D56474277BC0bD391846E8e580bE7C78"
erc721_contract = web3.eth.contract(address=contract_address, abi=abi)


def create():
    # 1
    nonce = web3.eth.getTransactionCount(
        "0xB00C8F28d9009CB4734612Df6c1c5b751194F2cA")
    tx = erc721_contract.functions.createAuction(
        "0x94b1bd2a4ACFa531C8C330c389072Cb08Db28108",
        70948226068845075091097172684116137139687598325071419309035027374095581839363,
        1000000,
        int(time.time())+100,
        int(time.time())+600
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


# create()


def bid():
    # 1
    nonce = web3.eth.getTransactionCount(
        PUBLIC_KEY)
    tx = erc721_contract.functions.bid(
        "0x94b1bd2a4ACFa531C8C330c389072Cb08Db28108",
        70948226068845075091097172684116137139687598325071419309035027374095581839363,
        2000000
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


# bid()


def update_end():
    # 1
    nonce = web3.eth.getTransactionCount(PUBLIC_KEY)
    tx = erc721_contract.functions.updateEndingTimestamp(
        "0x94b1bd2a4ACFa531C8C330c389072Cb08Db28108",
        70948226068845075091097172684116137139687598325071419309035027374095581839363,
        int(time.time())+300
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


# update_end()


def cancel():
    # 1
    nonce = web3.eth.getTransactionCount(PUBLIC_KEY)
    tx = erc721_contract.functions.cancelAuction(
        "0x94b1bd2a4ACFa531C8C330c389072Cb08Db28108",
        70948226068845075091097172684116137139687598325071419309035027374095581839363,
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


# cancel()


def end():
    # 1
    nonce = web3.eth.getTransactionCount(PUBLIC_KEY)
    tx = erc721_contract.functions.endAuction(
        "0x94b1bd2a4ACFa531C8C330c389072Cb08Db28108",
        70948226068845075091097172684116137139687598325071419309035027374095581839363,
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


# end()

abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            },
            {
                "name": "_spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "payable": True,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]
contract_address = "0xc778417E063141139Fce010982780140Aa0cD5Ab"
erc721_contract = web3.eth.contract(address=contract_address, abi=abi)


def approve_weth():
    # 1
    nonce = web3.eth.getTransactionCount(
        "0xB00C8F28d9009CB4734612Df6c1c5b751194F2cA")
    tx = erc721_contract.functions.approve(
        "0x52aFa4a1F861cAB8022bdcf053b523d9C1b75Ec2",
        2*10**6
    ).buildTransaction(
        {
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": web3.toWei("50", "gwei"),
        }
    )
    # 2
    signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
    # 3
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(web3.toHex(tx_hash))


# approve_weth()
