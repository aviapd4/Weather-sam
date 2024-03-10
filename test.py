import unittest
from unittest.mock import MagicMock
from .add_function import create_handler
from .delete_function import delete_handler


class TestLambdaFunctions(unittest.TestCase):
    def test_create_handler_allowme_in_payload(self):
        # Test setup
        event = {
            "body": '{"token": "allowme"}'
        }

        # Call the handler function
        response = create_handler(event, None)

        # Assert the response
        self.assertEqual(response['statusCode'], 200)  # Example assertion

    def test_delete_handler_allowme_in_payload(self):
        # Test setup
        event = {
            "body": '{"token": "allowme"}'
        }

        # Call the handler function
        response = delete_handler(event, None)

        # Assert the response
        self.assertEqual(response['statusCode'], 200)  # Example assertion

if __name__ == '__main__':
    unittest.main()
