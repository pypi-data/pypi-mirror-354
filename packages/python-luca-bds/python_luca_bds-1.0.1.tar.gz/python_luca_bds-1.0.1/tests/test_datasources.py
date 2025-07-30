from luca.datasources import get_datasources, get_datasource
import pytest
import pandas as pd

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_datasources(test_LucaConnector, return_pd, expected_type):
    result = get_datasources(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_datasource(test_LucaConnector, return_pd, expected_type):
    result = get_datasource(conn=test_LucaConnector, id=211488, return_pd=return_pd)
    assert isinstance(result, expected_type)