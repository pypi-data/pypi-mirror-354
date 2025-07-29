from http import HTTPStatus

import requests

from .scheme import AuthResponse


def auth(self, username, password):
    session = requests.Session()
    login_data = {
        'user': username,
        'password': password,
    }
    if self.proto == 'https':
        response = session.post(
            f'{self.base_url}/login',
            json=login_data,
            verify=self.verify,
        )
    if self.proto == 'http':
        response = session.post(
                f'{self.base_url}/login',
                json=login_data,
            )

    assert response.status_code == HTTPStatus.OK
    auth_response = AuthResponse(**response.json())
    token = auth_response.data.authToken
    uid = auth_response.data.me.id
    return token, uid


class Auth():
    def session(self, username, password):
        auth_token, uid = auth(self, username, password)
        session = requests.Session()
        headers = {
            'X-Auth-Token': auth_token,
            'X-User-Id': uid,
        }
        session.headers.update(headers)
        session.username = username
        session.uid = uid
        return session
