import json
import requests

SIGNUP_URL = "http://127.0.0.1:8000/signup/"
LOGIN_URL = "http://127.0.0.1:8000/login/"
TRANSACTION_URL = "http://127.0.0.1:8000/transaction/"
GET_BALANCE = "http://127.0.0.1:8000/get_balance/"


def signup():
    data = {
        'username': 'user2',
        'first_name': 'dhruv',
        'last_name': 'karandikar',
        'password': 'abcbab',
        'gender': 'm',
        'age': 20
    }
    headers = {'content-Type': 'application/json'}
    json_data = json.dumps(data)
    r = requests.post(url=SIGNUP_URL, headers=headers,data=json_data)
    new_data = r.json()
    print(new_data)


def login():
    data = {}
    json_data = json.dumps(data)
    r = requests.post(url=LOGIN_URL, data=json_data)
    new_data = r.json()
    print(new_data)


def transaction(id=None):
    pass


def get_balance(id=None):
    data = {}
    headers = {'content-Type': 'application/json'}
    if id is not None:
        data = {'id': id}
    json_data = json.dumps(data)
    r = requests.get(url=GET_BALANCE, headers=headers, data=json_data)
    data = r.json()
    print(data)


# signup()
# get_balance()
