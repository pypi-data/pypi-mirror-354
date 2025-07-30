from typing import Any, List, Type, Dict

from easyask.infras.chart.chart import Chart
from easyask.infras.chart.qwen_echarts import QwenEcharts


def get_chart_options(dataset: List[List[Any]], generator_cls: Type[Chart] = QwenEcharts, config: Dict = None):
    if config is None:
        config = {}

    generator = generator_cls(dataset, config)
    return generator.get_options()
