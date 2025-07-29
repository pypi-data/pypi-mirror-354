from enum import Enum
from typing import Optional

from gencrafter.core.metrics.column_metrics import ColumnCountsMetric, TypeCountersMetric
from gencrafter.core.metrics.condition_count_metric import ConditionCountMetric
from gencrafter.core.metrics.metrics import (
    CardinalityMetric,
    DistributionMetric,
    FrequentItemsMetric,
    IntsMetric,
    Metric,
    MetricConfig,
)
from gencrafter.core.metrics.unicode_range import UnicodeRangeMetric


class StandardMetric(Enum):
    types = TypeCountersMetric
    distribution = DistributionMetric
    counts = ColumnCountsMetric
    ints = IntsMetric
    cardinality = CardinalityMetric
    frequent_items = FrequentItemsMetric
    unicode_range = UnicodeRangeMetric
    condition_count = ConditionCountMetric

    def __init__(self, clz: Metric):
        self._clz = clz

    def zero(self, config: Optional[MetricConfig] = None) -> Metric:  # type: ignore
        config = config or MetricConfig()
        return self._clz.zero(config)
