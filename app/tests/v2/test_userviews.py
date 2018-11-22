import unittest
import json
from .data import no_data, data_1, data_2, data_3, data_4, \
    request_1, request_2, request_3, request_4, request_5,\
    request_6, request_7, request_8, request_9, request_reg, request_log
from ... import create_app


class ParcelModelCase(unittest.TestCase):
    """main test class"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def get_token(self):
        self.client.post('/api/v2/register', data=json.dumps(request_reg),
                         content_type='application/json')
        resp = self.client.post('/api/v2/login', data=json.dumps(request_log),
                                content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def test_create_order(self):
        """Tests if an order has been created"""
        res = self.client.post('/api/v2/parcels',
                               data=json.dumps(request_1),
                               content_type='application/json', headers=self.get_token())
        output = json.loads(res.data.decode())
        self.assertEqual(output['Status'], "created",
                         msg="Incomplete credentials not allowed")
        assert res.status_code == 201

    def test_get_all_orders(self):
        """Test get all functionality of an order"""
        res = self.client.get('/api/v1/parcels')
        self.assertTrue(res.status_code, 200)
