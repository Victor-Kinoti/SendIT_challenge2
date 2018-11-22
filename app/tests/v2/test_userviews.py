import unittest
import json
from db.db_config import destroy_tables
from db.create_tables import DatabaseConnection
from .data import no_data, data_1, data_2, data_3, data_4, \
    request_1, request_2, request_3, request_4, request_5,\
    request_6, request_7, request_8, request_9, request_reg, request_log
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
        # self.assertEqual(output['Status'], "created",
        #                  msg="Incomplete credentials not allowed")
        assert res.status_code == 201

    def test_get_all_orders(self):
        """Test get all functionality of an order"""
        res = self.client.get('/api/v2/parcels', headers=self.get_token())
        self.assertEqual(res.status_code, 200)

    def test_get_order_invalid_id(self):
        """Test when an invalid id is provided"""
        res = self.client.get('/api/v2/parcels/v')
        resp = json.loads(res.get_data())
        assert res.status_code == 400
        assert "bad request" in resp["Status"]
        assert "Provide a valid order id" in resp["Message"]

    def test_specific_order_not_found(self):
        """Test when an specific order is not found"""
        res = self.client.get('/api/v2/parcels/333', headers=self.get_token())
        resp = json.loads(res.get_data())
        assert "Not Found" in resp['Status']
        assert res.status_code == 404

    def test_one_user_data_not_found(self):
        """Test when orders of a specific user not found"""
        res = self.client.get('/api/v2/parcels/289',
                              headers=self.get_token())
        resp = json.loads(res.get_data())
        assert "Not Found" in resp['Status']
        # assert "User doesn't exist" in resp['Status']
        assert res.status_code == 404

    def test_one_user_data_found(self):
        """Tests when orders of specific user are found"""
        res = self.client.post("/api/v2/parcels",
                               data=json.dumps(request_1),
                               content_type='application/json', headers=self.get_token())
        res = self.client.get('/api/v1/users/keynote/parcels')
        resp = json.loads(res.get_data())
        assert res.status_code == 200

    def test_role_admin_user_only(self):
        """Test roles provided"""
        res = self.client.post("/api/v1/register",
                               data=json.dumps(request_9),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.status_code == 400
        assert res.content_type == 'application/json'
        assert output['Message'] == 'Roles can be either Admin or User'

    def test_pass_not_matching(self):
        """Test password and con_password not matching"""
        res = self.client.post("/api/v2/register",
                               data=json.dumps(request_3),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == \
            "Password and confirm password not matching"
        assert res.content_type == 'application/json'
        assert res.status_code == 400

    def test_username_missing(self):
        """Test username is not provided"""
        res = self.client.post("/api/v1/register",
                               data=json.dumps(request_4),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == \
            "Some or all fields are missing"
        assert res.content_type == 'application/json'
        assert res.status_code == 400

    def test_password_missing(self):
        """Test password not provided"""
        res = self.client.post("/api/v2/register",
                               data=json.dumps(request_5),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.content_type == 'application/json'
        assert output['message'] == \
            "Some or all fields are missing"
        assert res.status_code == 400

    def test_user_not_login(self):
        """Test registered user login"""
        res = self.client.post("/api/v2/login",
                               data=json.dumps(request_6),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['Status'] == 'Email/password wrong'
        assert res.status_code == 400

    def test_email_is_valid(self):
        """Test valid email format"""
        res = self.client.post("/api/v2/register",
                               data=json.dumps(request_8),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.status_code == 400
        assert output['message'] == "wrong email format"

    def test_email_missing(self):
        """Test email not provided"""
        res = self.client.post("/api/v2/register",
                               data=json.dumps(request_7),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == "Some or all fields are missing"
        assert res.content_type == 'application/json'
        assert res.status_code == 400

    def test_wrong_url(self):
        """Test email not provided"""
        res = self.client.get('/api/v2/parce', headers=self.get_token())
        output = json.loads(res.data.decode())
        assert res.status_code == 404
        assert output['Status'] == "Not Found"

    # def test_payment_status(self):
    #     """Test when payment status is updated"""
    #     res = self.client.put("/api/v2/users/paid/1",
    #                           data=json.dumps(data_1),
    #                           content_type='application/json')
    #     output = json.loads(res.data.decode())
    #     assert output['message'] == 'order paid!'
    #     assert res.status_code == 200

    # def test_delivered_status(self):
    #     """Test when delivered status is updated"""
    #     res = self.client.put("/api/v2/users/delivered/1",
    #                           data=json.dumps(data_1),
    #                           content_type='application/json')
    #     output = json.loads(res.data.decode())
    #     assert output['message'] == 'order has been delivered!'
    #     assert res.status_code == 200

    def test_address_fields(self):
        """Test all addresses are provided"""
        res = self.client.post("/api/v2/parcels",
                               data=json.dumps(data_3),
                               content_type='application/json', headers=self.get_token())
        output = json.loads(res.data.decode())
        assert output['message'] == \
            'ensure to provide the addresses in correct format'
        assert res.status_code == 400
