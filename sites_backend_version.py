import requests
import pytest

HEADERS = {'Content-Type': 'application/json'}
TEST_USER_EMAIL = "fh_ui_tester@test.test"
TEST_USER_PASSWORD = "Test1234"
DATA = {
    'email': TEST_USER_EMAIL,
    'password': TEST_USER_PASSWORD
}
auth_response = requests.post(url='https://cportal-beta-internal.futurehome.io/api/users/login',
                     json=DATA, headers=HEADERS)
token = auth_response.json()['token']
HEADERS['Authorization'] = 'Bearer {}'.format(token)


def send_site_detail_post(site_id, backend_version, headers=HEADERS):
    resp = requests.post('https://cportal-beta.futurehome.io/api/hub/sites/{}/backend/{}'.format(site_id,
                                                                                                   backend_version),
                         headers=headers, data='')
    print("Status:" + str(resp.status_code))
    print("Resp:" + str(resp.text))
    return resp


def test_backend_1_migration():
    resp = send_site_detail_post(7806, 1)
    assert resp.status_code == 204


def test_backend_2_migration():
    resp = send_site_detail_post(7806, 2)
    assert resp.status_code == 204


def test_backend_migration_wrong_token():
    headers = HEADERS
    headers['Authorization'] = "Bearer TEST_INCORRECT_TOKEN"
    resp = send_site_detail_post(7806, 2, headers)
    assert resp.status_code == 401


def test_backend_migration_invalid_id():
    resp = send_site_detail_post("TEST_INCORRECT_ID", 2)
    assert resp.status_code == 400


def test_backend_migration_empty_id():
    resp = send_site_detail_post("", 2)
    assert resp.status_code == 400


def test_backend_migration_invalid_backend_id():
    resp = send_site_detail_post(7806, "TEST_INCORRECT_ID")
    assert resp.status_code == 400


def test_backend_migration_empty_backend_id():
    resp = send_site_detail_post(7806, "")
    assert resp.status_code == 400
