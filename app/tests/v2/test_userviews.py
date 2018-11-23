import unittest
import json
from db.db_config import destroy_tables
from db.create_tables import DatabaseConnection
from .data import no_data, data_1, data_2, data_3, data_4, \
    request_1, request_2, request_3, request_4, request_5,\
    request_6, request_7, request_8, request_9, request_reg, request_log, request_reg2
from ... import create_app


class ParcelModelCase(unittest.TestCase):
    """main test class"""

    conn = DatabaseConnection()
    conn.create_tables()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def get_token(self):
        self.client.post('/api/v2/signup', data=json.dumps(request_reg),
                         content_type='application/json')
        resp = self.client.post('/api/v2/login', data=json.dumps(request_log),
                                content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def get_token2(self):
        self.client.post('/api/v2/signup', data=json.dumps(request_reg2),
                         content_type='application/json')
        resp = self.client.post('/api/v2/login', data=json.dumps(request_log),
                                content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def test_pass_not_matching(self):
        """Test password and con_password not matching"""
        res = self.client.post("/api/v2/signup",
                               data=json.dumps(request_3),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == \
            "Password and confirm password not matching"
        assert res.content_type == 'application/json'
        assert res.status_code == 400

    def test_password_missing(self):
        """Test password not provided"""
        res = self.client.post("/api/v2/signup",
                               data=json.dumps(request_5),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.content_type == 'application/json'
        assert output['message'] == \
            "Some or all fields are missing"
        assert res.status_code == 400

    def test_email_is_valid(self):
        """Test valid email format"""
        res = self.client.post("/api/v2/signup",
                               data=json.dumps(request_8),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.status_code == 400
        assert output['message'] == "wrong email format"

    def test_email_missing(self):
        """Test email not provided"""
        res = self.client.post("/api/v2/signup",
                               data=json.dumps(request_7),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == "Some or all fields are missing"
        assert res.content_type == 'application/json'
        assert res.status_code == 400

    def test_get_all_orders(self):
        res = self.client.get('/api/v2/parcels', headers=self.get_token())
        self.assertTrue(res.status_code, 200)
