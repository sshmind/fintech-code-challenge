from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
import json


class BustStockAPITests(TestCase):


    @patch('utils.helper_functions.Redis')
    def test_accepted_response(self, mock_redis):

        mock_client = mock_redis.return_value

        user_data = {'credit': 100}
        stock_data = {'price': [10, 20, 30]}
        mock_client.get.side_effect = lambda key: json.dumps(user_data) if key == 'user1' else json.dumps(stock_data)

        client = APIClient()
        response = client.post('/api/buy-stock/', data={'user': 'user1', 
                                                                  'stockname': 'stock1',
                                                                  'quantity': 1})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['msg'], 'ACCEPTED')
    
    @patch('utils.helper_functions.Redis')
    def test_low_user_credit(self, mock_redis):
        mock_client = mock_redis.return_value

        user_data = {'credit': 0}
        stock_data = {'price': [10, 20, 30]}
        mock_client.get.side_effect = lambda key: json.dumps(user_data) if key == 'user1' else json.dumps(stock_data)

        client = APIClient()
        response = client.post('/api/buy-stock/', data={'user': 'user1', 
                                                                  'stockname': 'stock1',
                                                                  'quantity': 1})
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['msg'], "Your credit for the purchase is low!")
    
    def test_api_serializer_for_invalid_user_account(self):

        client = APIClient()
        response = client.post('/api/buy-stock/', data={'user': 'user5', 
                                                                  'stockname': 'stock1',
                                                                  'quantity': 1})
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['user'][0], 'Invalid user account!')

    def test_api_serializer_for_invalid_stock_name(self):

        client = APIClient()
        response = client.post('/api/buy-stock/', data={'user': 'user1', 
                                                                  'stockname': 'stock9',
                                                                  'quantity': 1})
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['stockname'][0], 'Invalid stock name!')
