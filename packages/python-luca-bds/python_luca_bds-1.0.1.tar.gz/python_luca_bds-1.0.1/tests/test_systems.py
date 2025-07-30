from luca.systems import get_systems, get_system
import pytest
import pandas as pd

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_systems(test_LucaConnector, return_pd, expected_type):
    result = get_systems(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_system(test_LucaConnector, return_pd, expected_type):
    result = get_system(conn=test_LucaConnector, id=17002, return_pd=return_pd)
    assert isinstance(result, expected_type)