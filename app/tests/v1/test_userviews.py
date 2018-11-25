import unittest
import json
from .data import no_data, data_1, data_2, data_3,data_4, \
request_1, request_2, request_3, request_4, request_5,\
                    request_6, request_7, request_8, request_9
from ... import create_app
from ...api.v1.views import UserViews
from ...api.v1.models.UserModels import Order

class ParcelModelCase(unittest.TestCase):
    """main test class"""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()        

    def test_create_order(self):
        """Tests if an order has been created"""
        res = self.client.post('/api/v1/parcels', \
        data=json.dumps(request_1), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        self.assertEqual(output['Status'], "created",\
         msg="Incomplete credentials not allowed")
        assert res.status_code == 201

    def test_get_all_orders(self):
        """Test get all functionality of an order"""
        res = self.client.get('/api/v1/parcels')
        self.assertTrue(res.status_code, 200)


    def test_get_order_invalid_id(self):
        """Test when an invalid id is provided"""
        res = self.client.get('/api/v1/parcels/v')
        resp = json.loads(res.get_data())
        assert res.status_code == 400
        assert "bad request" in resp["Status"]
        assert "Provide a valid order id" in resp["Message"]

    def test_specific_order_not_found(self):
        """Test when an specific order is not found"""
        res = self.client.get('/api/v1/parcels/333')
        resp = json.loads(res.get_data())
        assert "Not Found" in resp['Status']
        assert res.status_code == 404

    def test_one_user_data_not_found(self):
        """Test when orders of a specific user not found"""
        res = self.client.get('/api/v1/users/keyvk/parcels')
        resp = json.loads(res.get_data())
        assert "Not Found" in resp['Status']
        assert "Resource not available!" in resp['Message']
        assert res.status_code == 400 

    def test_one_user_data_found(self):
        """Tests when orders of specific user are found"""
        res = self.client.post("/api/v1/parcels",\
         data=json.dumps(request_1), \
        content_type='application/json')
        res = self.client.get('/api/v1/users/keynote/parcels')
        resp = json.loads(res.get_data())
        assert res.status_code == 200              



    def test_invalid_order_id_cancels(self):
        """Test canceling an invalid order"""
        res = self.client.put('/api/v1/parcels/s/cancel', \
        data=json.dumps(request_1), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.status_code == 400
        self.assertEqual(output['Status'], 'bad request')
        assert "Provide a valid order id" in output['Message']        


    def test_register_user(self):
        """Test registering a new user"""
        res = self.client.post("/api/v1/register",\
         data=json.dumps(request_2), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.status_code == 201
        assert res.content_type == 'application/json;charset=utf-8'
        assert output['Status'] == 'User created'

    def test_role_admin_user_only(self):
        """Test roles provided"""
        res = self.client.post("/api/v1/register", \
        data=json.dumps(request_9), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.status_code == 400
        assert res.content_type == 'application/json'
        assert output['Message'] == 'Roles can be either Admin or User'

    def test_pass_not_matching(self):
        """Test password and con_password not matching"""
        res = self.client.post("/api/v1/register",\
         data=json.dumps(request_3), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == \
        "Password and confirm password not matching"
        assert res.content_type == 'application/json'
        assert res.status_code == 400

    def test_username_missing(self):
        """Test username is not provided"""
        res = self.client.post("/api/v1/register",\
         data=json.dumps(request_4), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == \
        "Some or all fields are missing"
        assert res.content_type == 'application/json'
        assert res.status_code == 400
        

    def test_password_missing(self):
        """Test password not provided"""
        res = self.client.post("/api/v1/register", \
        data=json.dumps(request_5), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.content_type == 'application/json'
        assert output['message'] == \
        "Some or all fields are missing"
        assert res.status_code == 400

    def test_user_login(self):
        """Test registered user login"""
        res = self.client.post("/api/v1/login", \
        data=json.dumps(request_6), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['Status'] == 'User Logged in'
        assert res.status_code == 201
        assert res.content_type == 'application/json;charset=utf-8'

    def test_email_is_valid(self):
        """Test valid email format"""
        res = self.client.post("/api/v1/register",\
         data=json.dumps(request_8), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert res.status_code == 400
        assert output['message'] == "wrong email format"


    def test_email_missing(self):
        """Test email not provided"""
        res = self.client.post("/api/v1/register", \
        data=json.dumps(request_7), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == "Some or all fields are missing"
        assert res.content_type == 'application/json'
        assert res.status_code == 400

    def test_payment_status(self):
        """Test when payment status is updated"""
        res = self.client.put("/api/v1/users/paid/1",\
         data=json.dumps(data_1), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == 'order paid!'
        assert res.status_code == 200

    def test_delivered_status(self):
        """Test when delivered status is updated"""
        res = self.client.put("/api/v1/users/delivered/1",\
         data=json.dumps(data_1), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == 'order has been delivered!'
        assert res.status_code == 200

    def test_address_fields(self):
        """Test all addresses are provided"""
        res = self.client.post("/api/v1/parcels", \
        data=json.dumps(data_3), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == \
        'ensure to provide the addresses in correct format'
        assert res.status_code == 400

    def test_recipient_fields_missing(self):
        """Test all recipeint fields are available"""
        res = self.client.post("/api/v1/parcels",\
         data=json.dumps(data_4), \
        content_type='application/json')
        output = json.loads(res.data.decode())
        assert output['message'] == \
        'recipient_name or recipient_id missing or wrong data format'
        assert res.status_code == 400       




if __name__ == '__main__':
    unittest.main()