from luca.querys import query, get_queries, get_query, execute_query
import pytest
import pandas as pd

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_get_queries(test_LucaConnector, return_pd, expected_type):
    result = get_queries(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_get_query(test_LucaConnector, return_pd, expected_type):
    result = get_query(conn=test_LucaConnector, id=364, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_execute_query(test_LucaConnector, return_pd, expected_type):
    result, pag, state = execute_query(
        conn=test_LucaConnector,
        id=364,
        environment_id=1,
        input_variables=[
            {'id': 6458, 'key': "USER", 'type': "string", 'value': "admin\ndemo"},
            {'id': 366, 'key': "SISTEMA", 'type': "string", 'value': "LUCA"}
        ],
        return_pd=return_pd
    )
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_query_id(test_LucaConnector, return_pd, expected_type):
    result, pag, state = query(
        conn=test_LucaConnector,
        id=364,
        environment='DES',
        input_variables=[{'Usuario': 'luca', 'Sistema': 'LUCA'}],
        return_pd=return_pd
    )
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_query(test_LucaConnector, return_pd, expected_type):
    result, pag, state = query(
        conn=test_LucaConnector,
        name='Prueba',
        environment='DES',
        return_pd=return_pd
    )
    assert isinstance(result, expected_type)