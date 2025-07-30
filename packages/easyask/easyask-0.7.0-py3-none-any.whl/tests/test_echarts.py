import json

import pytest

from easyask.tools import chart


@pytest.mark.skip(reason="This test is skipped since api key reason")
def test_echarts_options():
    options = chart.get_chart_options([
        ['Matcha Latte', 43.3, 85.8, 93.7],
        ['Milk Tea', 83.1, 73.4, 55.1],
        ['Cheese Cocoa', 86.4, 65.2, 82.5],
        ['Walnut Brownie', 72.4, 53.9, 39.1]
    ], ['product', '2015', '2016', '2017'])

    print(options)

    assert json.loads(options) is not None
