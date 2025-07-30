"""
Unit tests for blockchain transactions and utilities.

This module contains unit tests for the BlockchainTransaction and
TransactionUtils classes.
"""

import unittest
from unittest.mock import MagicMock, patch

from blockchain.transaction import BlockchainTransaction, ProviderManager
from blockchain.utils import TransactionUtils


class TestBlockchainTransaction(unittest.TestCase):
    """
    Test cases for the BlockchainTransaction class.
    """

    @patch.object(ProviderManager, 'get_web3_instance')
    def test_get_balance(self, mock_get_web3_instance):
        """
        Test the get_balance method.
        """
        mock_web3 = MagicMock()
        mock_get_web3_instance.return_value = mock_web3
        mock_web3.toChecksumAddress.return_value = '0xChecksumAddress'
        mock_web3.eth.getBalance.return_value = 1000

        balance = BlockchainTransaction.get_balance('ethereum_mainnet', '0xAddress')
        self.assertEqual(balance, 1000)

    @patch.object(BlockchainTransaction, 'get_balance')
    def test_ensure_balance(self, mock_get_balance):
        """
        Test the ensure_balance method.
        """
        mock_get_balance.return_value = 2000
        result = BlockchainTransaction.ensure_balance('ethereum_mainnet', '0xAddress', 1, 1000)
        self.assertTrue(result)

    @patch.object(ProviderManager, 'get_web3_instance')
    def test_get_address_nonce(self, mock_get_web3_instance):
        """
        Test the get_address_nonce method.
        """
        mock_web3 = MagicMock()
        mock_get_web3_instance.return_value = mock_web3
        mock_web3.toChecksumAddress.return_value = '0xChecksumAddress'
        mock_web3.eth.getTransactionCount.return_value = 5

        nonce = BlockchainTransaction.get_address_nonce('ethereum_mainnet', '0xAddress')
        self.assertEqual(nonce, 5)

    def test_get_chaincode(self):
        """
        Test the get_chaincode method.
        """
        chaincode = BlockchainTransaction.get_chaincode('ethereum_mainnet')
        self.assertEqual(chaincode, 1)

    @patch.object(ProviderManager, 'get_web3_instance')
    def test_create_transaction(self, mock_get_web3_instance):
        """
        Test the create_transaction method.
        """
        mock_web3 = MagicMock()
        mock_get_web3_instance.return_value = mock_web3
        mock_web3.toChecksumAddress.return_value = '0xChecksumAddress'

        metadata = {
            'chain': 'ethereum_mainnet',
            'toaddress': '0xAddress',
            'gasprice': 1,
            'gaslimit': 21000,
            'value': 1000
        }
        tx = BlockchainTransaction.create_transaction(
            b'blockchain_bytes', metadata, 'nonce_data', 1)
        self.assertEqual(tx['nonce'], 'nonce_data')
        self.assertEqual(tx['gasPrice'], 1)
        self.assertEqual(tx['gas'], 21000)
        self.assertEqual(tx['to'], '0xChecksumAddress')
        self.assertEqual(tx['value'], 1000)
        self.assertEqual(tx['data'], b'blockchain_bytes')
        self.assertEqual(tx['chainId'], 1)
        self.assertEqual(tx['from'], '0xChecksumAddress')

class TestTransactionUtils(unittest.TestCase):
    """
    Test cases for the TransactionUtils class.
    """

    def test_generate_transaction_id(self):
        """
        Test the generate_transaction_id method.
        """
        transaction_id = TransactionUtils.generate_transaction_id()
        self.assertTrue(isinstance(transaction_id, str))
        self.assertEqual(len(transaction_id), 36)

    @patch('blockchain.utils.BlockchainTransaction')
    def test_create_transaction(self, MockBlockchainTransaction):
        """
        Test the create_transaction method.
        """
        mock_transaction = MockBlockchainTransaction.return_value
        transaction = TransactionUtils.create_transaction('0xFromAddress', '0xToAddress', 100.0)
        self.assertEqual(transaction, mock_transaction)

if __name__ == '__main__':
    unittest.main()
