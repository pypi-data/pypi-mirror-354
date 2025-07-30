from luca.connectors import LucaConnector, KeycloakConnector
import pytest
import pandas as pd

keycloak_env = {
    'server_url': 'https://dev.luca-bds.com/auth',
    'realm_name': 'luca-bds',
    'client_id': 'luca-bds-web'
}

luca_env = {
    'server_url': 'https://dev.luca-bds.com/luca-api',
    'username': 'user',
    'password': 'pass'
}

@pytest.fixture
def test_KeycloakConnector():
    return KeycloakConnector(**keycloak_env)

@pytest.fixture
def test_KeycloakLucaConnector(test_KeycloakConnector):
    return LucaConnector(keycloak_connection=test_KeycloakConnector, **luca_env)

@pytest.fixture
def test_LucaConnector():
    return LucaConnector(**luca_env)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_info_kc(test_KeycloakLucaConnector, return_pd, expected_type):
    result = test_KeycloakLucaConnector.info(return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_info(test_LucaConnector, return_pd, expected_type):
    result = test_LucaConnector.info(return_pd=return_pd)
    assert isinstance(result, expected_type)