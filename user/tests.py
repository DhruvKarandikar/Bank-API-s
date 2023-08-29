import copy
import logging
import random
from atm.settings import SECRET_KEY
from .models import User
from walletApp.models import Account
from django.test import TestCase, Client
from django.urls import reverse
import json
import jwt
import mock
import requests_mock
import requests
logger = logging.getLogger("django")


def user_create(**kwargs):
    return User.objects.create(**kwargs)


def user_account_create(user, account_id):
    return Account.objects.create(user, account_id)


# def create_token(user_obj):
#     get_user_id = jwt.encode(jwt=user_obj.get('access'), key=SECRET_KEY, algorithms=['HS256'])
#     print(get_user_id)
#     return get_user_id['user_id']


def generate_account_number():
    return random.randint(2004, 5000)


class TestSignupView(TestCase):
    data = {
        "username": "AloneHUGER",
        "first_name": "Hugh",
        "last_name": "Jackman",
        "password": "ABCabc12333",
        "gender": "F",
        "age": 15
    }

    def setUp(self):
        self.client = Client()  # It provides methods that allow you to GET, POST, PUT, DELETE, and other types of requests
        self.url = reverse('signup-user')  # url name

    def postreq(self, payload):
        data = self.client.post(self.url, json.dumps(payload), content_type="application/json")
        content = json.loads(data.content)
        return content

    def test_data_created(self):
        data_copy = copy.deepcopy(self.data)
        data_copy['age'] = 25  # change the data value of a key
        expected_response = 'Data created'  # my expected response
        actual_response = self.postreq(data_copy)  # the response that I got from the code
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)

    def test_age_validate(self):
        data_copy = copy.deepcopy(self.data)
        expected_response = {
            'non_field_errors': ['age must be greater than 18 to open account']}  # my expected response
        actual_response = self.postreq(data_copy)  # the response that I got from the code
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)

    def test_username_taken(self):
        user_create(username=self.data.get('username'))
        data_copy = copy.deepcopy(self.data)
        data_copy['age'] = 21
        expected_response = {'msg': 'username taken'}  # my expected response
        actual_response = self.postreq(data_copy)  # the response that I got from the code
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)


class TestLoginView(TestCase):
    data = {
        "username": "AloneHUGER",
        "password": "ABCabc12333"
    }

    def setUp(self):
        self.client = Client()  # It provides methods that allow you to GET, POST, PUT, DELETE, and other types of requests
        self.url = reverse('login-user')  # url name

    def postreq(self, payload):
        data = self.client.post(self.url, json.dumps(payload), content_type="application/json")
        content = json.loads(data.content)
        return content

    def test_user_logged_in(self):
        data_copy = copy.deepcopy(self.data)
        user_obj = user_create(username=self.data.get('username'), password=self.data.get('password'))
        expected_response = user_obj.id
        actual_response_id = self.postreq(data_copy)  # the response that I got from the code
        actual_response_get = jwt.decode(jwt=actual_response_id.get('access'), key=SECRET_KEY, algorithms=['HS256'])
        actual_response = actual_response_get['user_id']
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)

    def test_user_or_pass_incorrect(self):
        user_create(username=self.data.get('username'), password=self.data.get('password'))
        data_copy = copy.deepcopy(self.data)
        data_copy['username'] = 'fhhfcfjjcfjcf'
        data_copy['password'] = 'tjckmtftkuhgv'
        expected_response = {'msg': 'Username or Password is Incorrect'}  # my expected response
        actual_response = self.postreq(data_copy)  # the response that I got from the code
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)

    def test_user_or_pass_blank(self):
        user_create(username=self.data.get('username'), password=self.data.get('password'))
        data_copy = copy.deepcopy(self.data)
        data_copy['username'] = ''
        data_copy['password'] = ''
        expected_response = {'password': ['This field may not be blank.'],
                             'username': ['This field may not be blank.']}  # my expected response
        actual_response = self.postreq(data_copy)  # the response that I got from the code
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)


class TestTransactionView(TestCase):
    data = {
        "account": 1,
        "transaction_type": 1,
        "transaction_balance": 3000
    }

    def setUp(self):
        self.client = Client()  # It provides methods that allow you to GET, POST, PUT, DELETE, and other types of requests
        self.url = reverse('balance-func')  # url name

    def postreq(self, payload):

        user_obj = user_create(username='Dhruv', password="1234567890")
        account = Account.objects.create(id=self.data.get('account'), user_id=user_obj.id,
                                         account_no=generate_account_number())
        token = jwt.encode({'user_id': user_obj.id}, SECRET_KEY, algorithm='HS256')
        headers = {"Authorization": f"Bearer {token}"}
        data = self.client.post(self.url, json.dumps(payload), content_type="application/json", headers=headers)
        content = json.loads(data.content)
        # with requests_mock.Mocker() as m:
        #     m.post("https://www.gov.uk/bank-holidays.json", json={}, status_code=200)
        #     response = self.postreq(content)
        return content, account, user_obj, # response

    # userid will be acquired from the jwt token
    def test_user_deposit(self):
        data_copy = copy.deepcopy(self.data)
        expected_response = {'msg': 'Account updated'}
        actual_response, account, u,  = self.postreq(data_copy)  # the response that I got from the code
        acc_bal = Account.objects.get(id=account.id, user_id=u)
        ini_bal = acc_bal.balance
        account.refresh_from_db()  # refreshes my database and gives updated value
        actual_balance = ini_bal
        expected_balance = acc_bal.balance
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        logger.debug("expected_balance: %s", expected_balance)
        logger.debug("actual_balance : %s", actual_balance)
        self.assertEqual(expected_response, actual_response)
        self.assertEqual(expected_balance, actual_balance)

    def test_user_exception_raise_deposit(self):
        user_obj = user_create(username='DhruvDex', password="qwerty")
        Account.objects.create(id=2, user_id=user_obj.id,
                               account_no=generate_account_number())
        data_copy = copy.deepcopy(self.data)
        data_copy['account'] = 2
        expected_response = {"error": "account not found"}
        actual_response, account, user_obj, = self.postreq(data_copy)  # the response that I got from the code
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)

    def test_user_exception_raise_withdraw(self):
        user_obj = user_create(username='DhruvDex', password="qwerty")
        Account.objects.create(id=2, user_id=user_obj.id,
                               account_no=generate_account_number())
        data_copy = copy.deepcopy(self.data)
        data_copy['account'] = 2
        data_copy['transaction_type'] = 2
        expected_response = {"error": "account not found"}
        actual_response, account, user_obj, = self.postreq(data_copy)  # the response that I got from the code
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)

    def test_user_withdraw(self):
        data_copy = copy.deepcopy(self.data)
        data_copy['transaction_type'] = 2
        expected_response = {'msg': 'Account updated'}
        actual_response, account, u, = self.postreq(data_copy)  # the response that I got from the code
        acc_bal = Account.objects.get(id=account.id, user_id=u)
        ini_bal = acc_bal.balance
        account.refresh_from_db()
        actual_balance = ini_bal
        expected_balance = acc_bal.balance
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        logger.debug("expected_balance: %s", expected_balance)
        logger.debug("actual_balance : %s", actual_balance)
        self.assertEqual(expected_response, actual_response)
        self.assertEqual(expected_balance, actual_balance)


class TestGetBalanceView(TestCase):
    acc_no = generate_account_number()
    data = {
        "account_no": acc_no,
        "balance": 1000
    }

    def setUp(self):
        self.client = Client()  # It provides methods that allow you to GET, POST, PUT, DELETE, and other types of requests
        # self.url = "http://127.0.0.1:8000/get_balance/"  # url name

    def getreq(self):
        user_obj = user_create(username='Dhruv', password="1234567890")
        account = Account.objects.create(user_id=user_obj.id, account_no=self.data.get('account_no'),
                                         balance=self.data.get('balance'))
        token = jwt.encode({'user_id': user_obj.id}, SECRET_KEY, algorithm='HS256')
        headers = {'Authorization': f'Bearer {token}', 'content_type': 'application/json'}
        data = self.client.get(path="http://127.0.0.1:8000/get_balance/", params=self.data, headers=headers)
        content = json.loads(data.content)
        return content, account, user_obj

    # userid will be acquired from the jwt token
    def test_user_get_balance(self):
        # data_copy = copy.deepcopy(self.data)
        actual_response, account, user_obj = self.getreq()  # the response that I got from the code
        acc_bal = Account.objects.get(user_id=user_obj.id)
        ini_bal = acc_bal.balance
        actual_balance = ini_bal
        expected_response = {'msg': {"account_no": self.data.get('account_no'), "balance": actual_balance}}
        logger.debug("expected_response: %s", expected_response)
        logger.debug("actual_response : %s", actual_response)
        self.assertEqual(expected_response, actual_response)

