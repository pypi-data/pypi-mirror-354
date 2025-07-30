"""
Utility functions for blockchain transactions.

This module provides utility functions for creating and managing blockchain transactions.
"""

import uuid
from .transaction import BlockchainTransaction

class TransactionUtils:
    """
    Utility class for blockchain transactions.

    This class includes methods for:
    - Creating a transaction
    - Generating a unique transaction ID
    """

    @staticmethod
    def create_transaction(from_address: str,
        to_address: str, amount: float) -> BlockchainTransaction:
        """
        Create a blockchain transaction.

        Args:
            from_address (str): The sender's address.
            to_address (str): The recipient's address.
            amount (float): The amount to be transferred.

        Returns:
            BlockchainTransaction: The created blockchain transaction.
        """
        id = TransactionUtils.generate_transaction_id()
        return BlockchainTransaction(id, from_address, to_address, amount)

    @staticmethod
    def generate_transaction_id() -> str:
        """
        Generate a unique transaction ID.

        Returns:
            str: A unique transaction ID.
        """
        return str(uuid.uuid4())
