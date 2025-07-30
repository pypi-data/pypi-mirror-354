from luca.charts import get_charts, get_chart
import pytest
import pandas as pd

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.DataFrame), (False, list)])
def test_charts(test_LucaConnector, return_pd, expected_type):
    result = get_charts(conn=test_LucaConnector, return_pd=return_pd)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("return_pd, expected_type", [(True, pd.Series), (False, dict)])
def test_chart(test_LucaConnector, return_pd, expected_type):
    result = get_chart(conn=test_LucaConnector, id=27133, return_pd=return_pd)
    assert isinstance(result, expected_type)