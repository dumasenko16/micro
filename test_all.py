import requests
import pytest
import json
import pprint


BASE_URL = 'http://localhost:8080'


@pytest.mark.parametrize(
    'endpoint',
    [
        '/v1/delivery',
        '/v1/data'
     ]
)
def test_two_endpoints(endpoint):
    response = requests.get(BASE_URL + endpoint)
    assert response.status_code == 200
    with open('output.txt', 'a') as file:
        pprint.pprint(
            json.loads(response.content.decode()),
            stream=file
        )


def test_protected_endpoint():
    headers = {
        'accept': 'application/json',
    }

    data = {
        'grant_type': '',
        'username': 'string',
        'password': 'string',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }
    urls = {
        'login': f'{BASE_URL}/v1/login',
        'users': f'{BASE_URL}/v1/users',
    }
    with open('output.txt', 'a') as file:
        response = requests.post(urls['login'], headers=headers, data=data)
        assert response.status_code == 200
        user_access_token = json.loads(response.content.decode())['access_token']
        assert user_access_token != ''
        headers['Authorization'] = f'Bearer {user_access_token}'
        data = json.loads(response.content.decode())
        data["status_code"] = response.status_code
        pprint.pprint(
            data,
            stream=file
        )
        response = requests.get(urls['users'])
        assert response.status_code == 401
        data = {}
        data["status_code"] = response.status_code
        pprint.pprint(
            data,
            stream=file
        )
        response = requests.get(urls['users'], headers=headers)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        data["status_code"] = response.status_code
        pprint.pprint(
            data,
            stream=file
        )

    #датасурсы ui не ui
    #в интерфейсе таргеты
    #в егере агрегированный запрос
    # как хелзчек