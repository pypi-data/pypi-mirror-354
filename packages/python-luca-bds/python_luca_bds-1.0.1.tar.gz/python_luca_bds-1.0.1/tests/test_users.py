from luca.users import get_users, get_user
import pytest
import pandas as pd

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_users(test_LucaConnector, return_pd, expected_type):
    result = get_users(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_user(test_LucaConnector, return_pd, expected_type):
    result = get_user(conn=test_LucaConnector, id=295054, return_pd=return_pd)
    assert isinstance(result, expected_type)