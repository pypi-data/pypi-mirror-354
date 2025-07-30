"""
Connector File for Blockchain Transactions

This module provides functions for interacting with blockchain networks, including:
- Checking account balance
- Ensuring minimum balance for transactions
- Getting address nonce
- Creating, signing, and sending transactions

It relies on a ProviderManager class to manage Web3 instances for different chains.
"""

from web3 import Web3

from .constants import (ETHEREUM_MAINNET_RPC, ETHEREUM_SEPOLIA_RPC,
                        POLY_AMOY_TESTNET_RPC, POLYGON_MAINNET_RPC,
                        POLYGON_TESTNET_RPC)
from .errors import (BroadcastError, InsufficientBalanceError,
                     SignTransactionError)


class ProviderManager:
    """
    Class to manage Web3 instances for different blockchain networks.

    Attributes:
        provider_url (dict): Dictionary mapping blockchain names to their RPC URLs.
    """

    def __init__(self):
        self.provider_url = {
            "ethereum_mainnet": ETHEREUM_MAINNET_RPC,
            "ethereum_sepolia": ETHEREUM_SEPOLIA_RPC,
            "polygon_mainnet": POLYGON_MAINNET_RPC,
            "polygon_testnet": POLYGON_TESTNET_RPC,
            "polygon_amoy": POLY_AMOY_TESTNET_RPC,
        }

    def get_web3_instance(self, chain):
        """
        Retrieve a Web3 instance for a given blockchain network.

        Args:
            chain (str): Name of the blockchain network.

        Returns:
            Web3: Instance of Web3 connected to the specified network.
        """
        if chain in self.provider_url:
            return Web3(Web3.HTTPProvider(self.provider_url[chain]))
        else:
            raise ValueError(f"Chain '{chain}' not found in provider_url dictionary.")


class BlockchainTransaction:
    """
    Class providing static methods for blockchain transactions.

    This class includes methods for:
    - Getting the balance of an address
    - Ensuring sufficient balance for transactions
    - Getting the nonce of an address
    - Creating, signing, and sending transactions
    - Getting the chain code for a blockchain network
    """

    @staticmethod
    def get_balance(chain: str, address: str):
        """
        Get the balance of an address in a given blockchain network.

        Args:
            chain (str): Name of the blockchain network.
            address (str): Ethereum address.

        Returns:
            int: Balance of the address in Wei.
        """
        try:
            web3 = ProviderManager().get_web3_instance(chain)
            checksum_address = web3.toChecksumAddress(address)
            balance = web3.eth.getBalance(checksum_address)
            return balance
        except Exception as e:
            return None

    @staticmethod
    def ensure_balance(chain: str, address: str, gas_price: int, gas_limit: int):
        """
        Ensure that the address has sufficient balance to cover transaction costs.

        Args:
            chain (str): Name of the blockchain network.
            address (str): Ethereum address.
            gas_price (int): Gas price for the transaction.
            gas_limit (int): Gas limit for the transaction.

        Returns:
            bool: True if the balance is sufficient, False otherwise.
        """
        # Check address balance
        balance = BlockchainTransaction.get_balance(chain, address)

        # Calculate the required transaction cost
        transaction_cost = gas_price * gas_limit

        if not balance or transaction_cost > balance:
            raise InsufficientBalanceError("Insufficient balance for transaction.")

        return True

    @staticmethod
    def get_address_nonce(chain: str, address: str):
        """
        Get the nonce (transaction count) for an address.

        Args:
            chain (str): Name of the blockchain network.
            address (str): Ethereum address.

        Returns:
            int: Nonce (transaction count) of the address.
        """
        try:
            web3 = ProviderManager().get_web3_instance(chain)
            checksum_address = web3.toChecksumAddress(address)
            nonce = web3.eth.getTransactionCount(checksum_address)
            return nonce
        except Exception as e:
            return 0

    @staticmethod
    def create_transaction(
        blockchain_bytes: bytes, metadata: dict, nonce_data: str, chain_id: int
    ):
        """
        Create a transaction object for sending on the blockchain network.

        Args:
            blockchain_bytes (bytes): Credential hash data in bytes.
            metadata (dict): Required data for the transaction.
            nonce_data (str): Nonce data for the transaction.
            chain_id (int): ID of the blockchain network.

        Returns:
            dict: Transaction object.
        """
        web3 = ProviderManager().get_web3_instance(metadata["chain"])
        checksum_address = web3.toChecksumAddress(metadata["toaddress"])
        tx = {
            "nonce": nonce_data,
            "gasPrice": metadata["gasprice"],
            "gas": metadata["gaslimit"],
            "to": checksum_address,
            "value": metadata["value"],
            "data": blockchain_bytes,
            "chainId": chain_id,
            "from": checksum_address,
        }

        return tx

    @staticmethod
    def get_chaincode(chain: str):
        """
        Get the chain code for a given blockchain network.

        Args:
            chain (str): Name of the blockchain network.

        Returns:
            int: Chain code.
        """
        # Dict of chain with their chain codes
        chaincodes = {
            "ethereum_mainnet": 1,
            "ethereum_ropsten": 3,
            "ethereum_sepolia": 11155111,
            "polygon_mainnet": 137,
            "polygon_testnet": 80001,
            "polygon_amoy": 80002,
            "evrc_chain": 5493,
        }

        # Get chain code of selected chain
        chaincode = chaincodes[chain]

        return chaincode

    @staticmethod
    def sign_transactions(prepared_tx: dict, skey: str, chain: str):
        """
        Sign a transaction using the private key.

        Args:
            prepared_tx (dict): Transaction object with required transaction data.
            skey (str): Secret key of the address.
            chain (str): Name of the blockchain network.

        Returns:
            object: Signed transaction object.
        """
        # Decrypt secret key
        # WEB3_SECRET_KEY

        # try to sign the transaction.
        try:
            web3 = ProviderManager().get_web3_instance(chain)

            # Sign the transaction
            signed_tx = web3.eth.account.sign_transaction(prepared_tx, skey)

            return signed_tx

        except Exception as msg:
            raise SignTransactionError(str(msg))

    @staticmethod
    def send_transaction(signed_tx: str, chain: str):
        """
        Send a signed transaction to the blockchain network.

        Args:
            signed_tx (str): Signed transaction object.
            chain (str): Name of the blockchain network.

        Returns:
            str: Transaction hash.
        """
        try:
            web3 = ProviderManager().get_web3_instance(chain)

            # Send the raw transaction
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            return tx_hash.hex()

        except Exception as e:
            raise BroadcastError("Error broadcasting the transaction")

    @staticmethod
    def issue_transaction(blockchain_bytes: bytes, metadata: dict, nonce: str):
        """
        Issue and send a blockchain transaction.

        Args:
            blockchain_bytes (bytes): Blockchain transaction RLP.
            metadata (dict): Dictionary of the required details.
            nonce (str): Nonce data for the transaction.

        Returns:
            str: Blockchain transaction hash.
        """
        # Get chaincode of chain
        netcode = BlockchainTransaction.get_chaincode(metadata["chain"])

        # Create transaction
        prepared_tx = BlockchainTransaction.create_transaction(
            blockchain_bytes, metadata, nonce, netcode
        )

        # Sign transaction
        tx_hex = BlockchainTransaction.sign_transactions(
            prepared_tx=prepared_tx, skey=metadata["skey"], chain=metadata["chain"]
        )

        # TODO: Add verify transaction
        # Send Transaction
        tx_hash = BlockchainTransaction.send_transaction(tx_hex, metadata["chain"])

        return tx_hash
