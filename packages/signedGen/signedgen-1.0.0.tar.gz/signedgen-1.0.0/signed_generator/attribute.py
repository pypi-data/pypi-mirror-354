from enum import Enum


class IssuerModeType(str, Enum):
    # Enums can be defined here
    ethereum_ropsten = "ethereum_ropsten"
    ethereum_mainnet = "ethereum_mainnet"
    ethereum_sepolia = "ethereum_sepolia"
    polygon_testnet = "polygon_testnet"
    polygon_mainnet = "polygon_mainnet"
    polygon_amoy = "polygon_amoy"
