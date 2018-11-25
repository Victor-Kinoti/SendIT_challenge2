import unittest
import json
from db.db_config import destroy_tables
from db.create_tables import DatabaseConnection
from .data import no_data, data_1, data_2, data_3, data_4, \
    request_1, request_2, request_3, request_4, request_5,\
    request_6, request_7, request_8, request_9, request_reg,\
    request_log, request_log2, request_log_non, request_reg2,\
    update_status, update_status_wrng, update_loc, update_dest
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

    def get_token(self):  # admin
        self.client.post('/api/v2/signup', data=json.dumps(request_reg),
                         content_type='application/json')
        resp = self.client.post('/api/v2/login', data=json.dumps(request_log),
                                content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def get_token2(self):  # user
        self.client.post('/api/v2/signup', data=json.dumps(request_reg2),
                         content_type='application/json')
        resp = self.client.post('/api/v2/login', data=json.dumps(request_log2),
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
        assert output['Status'] == \
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
        assert output['Status'] == \
            "password/con-password fields missing"
        assert res.status_code == 400

    def test_email_is_valid(self):
        """Test valid email format"""
        res = self.client.post("/api/v2/signup",
                               data=json.dumps(request_8),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.status_code == 400
        assert output['Status'] == "Email fields missing/ wrong email format"

    def test_email_missing(self):
        """Test email not provided"""
        res = self.client.post("/api/v2/signup",
                               data=json.dumps(request_7),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['Status'] == "Email fields missing/ wrong email format"
        assert res.content_type == 'application/json'
        assert res.status_code == 400

    def test_get_all_orders_unathorized(self):
        res = self.client.get('/api/v2/parcels', headers=self.get_token2())
        self.assertTrue(res.status_code, 200)
        output = json.loads(res.data.decode())
        assert output["Status"] == "Not Authorized!"
        assert res.status_code == 401

    def test_get_all_orders(self):
        res = self.client.get('/api/v2/parcels', headers=self.get_token())
        self.assertTrue(res.status_code, 200)
        output = json.loads(res.data.decode())
        assert output["Status"] == "Ok"

    def test_get_one_admin_users_order(self):
        res = self.client.get("/api/v2/parcels/1/orders",
                              content_type='application/json', headers=self.get_token())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Found user 1 orders"
        assert res.status_code == 200

    def test_get_one_order(self):
        res = self.client.get("/api/v2/orders/1",
                              content_type='application/json', headers=self.get_token())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Order found"
        assert res.status_code == 200

    def test_login_existing_user(self):
        res = self.client.post("/api/v2/login",
                               data=json.dumps(request_log),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "User Logged in"
        assert res.status_code == 200

    def test_login_non_existing_user(self):
        res = self.client.post("/api/v2/login",
                               data=json.dumps(request_log_non),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Email/password wrong"
        assert res.status_code == 404

    def test_successful_signup(self):
        res = self.client.post("/api/v2/signup",
                               data=json.dumps(request_9),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "User Keynote created"
        assert res.status_code == 201

    def test_unsuccessful_signup(self):
        res = self.client.post("/api/v2/signup",
                               data=json.dumps(request_9),
                               content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "User with that email already exists"
        assert res.status_code == 400

    def test_create_parcel_order(self):
        res = self.client.post("/api/v2/parcels",
                               data=json.dumps(request_1),
                               content_type='application/json', headers=self.get_token2())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "created"
        assert res.status_code == 201

    def test_unauthorized_create_parcel_order(self):
        res = self.client.post("/api/v2/parcels",
                               data=json.dumps(request_1),
                               content_type='application/json', headers=self.get_token())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Not Authorized!"
        assert res.status_code == 401

    def test_update_order_status(self):
        res = self.client.put("/api/v2/parcel/1/orders",
                              data=json.dumps(update_status),
                              content_type='application/json', headers=self.get_token())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Order Canceled"
        assert res.status_code == 200

    def test_update_location(self):
        res = self.client.put("/api/v2/parcels/1/presentLocation",
                              data=json.dumps(update_loc),
                              content_type='application/json', headers=self.get_token())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Current Location is Kisumu"
        assert res.status_code == 200

    def test_update_destination(self):
        res = self.client.put("/api/v2/parcels/1/destination",
                              data=json.dumps(update_dest),
                              content_type='application/json', headers=self.get_token2())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Destination updated to Kisumu"
        assert res.status_code == 200

    def test_update_order_status_wrong_status(self):
        res = self.client.put("/api/v2/parcel/1/orders",
                              data=json.dumps(update_status_wrng),
                              content_type='application/json', headers=self.get_token())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Status can be 'Canceled', 'Delivered' or 'In-Transit'"
        assert res.status_code == 400

    def test_get_users_history(self):
        res = self.client.get("/api/v2/parcels/1",
                              content_type='application/json', headers=self.get_token2())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Ok"
        assert res.status_code == 200

    def test_get_one_users_order(self):
        res = self.client.get("/api/v2/parcels/1/1",
                              content_type='application/json', headers=self.get_token2())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Your Order"
        assert res.status_code == 200

    def test_get_users_history(self):
        res = self.client.get("/api/v2/parcels/1",
                              content_type='application/json', headers=self.get_token2())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "Your Order History"
        assert res.status_code == 200

    def test_url_not_existing(self):
        res = self.client.get("/api/v2/parcels/jj",
                              content_type='application/json', headers=self.get_token2())
        output = json.loads(res.data.decode())
        assert output['Status'] == \
            "URL doesn't exist"
        assert res.status_code == 404

    conn.destroy_tables()
