"""
Custom error classes for the Transactify package.
"""

class BlockchainError(Exception):
    """Base class for all blockchain-related errors."""


class BroadcastError(BlockchainError):
    """Raised when there is an error broadcasting a transaction."""


class SignTransactionError(BlockchainError):
    """Raised when there is an error signing a transaction."""


class InsufficientBalanceError(BlockchainError):
    """Raised when there is insufficient balance for a transaction."""
