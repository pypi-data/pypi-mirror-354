from typing import List

from gencrafter.core.constraints.factories import column_is_probably_unique
from gencrafter.core.constraints.metric_constraints import MetricConstraint
from gencrafter.core.utils import is_probably_unique
from gencrafter.core.utils.stats_calculations import only_null_values
from gencrafter.core.view.column_profile_view import ColumnProfileView


def generate_column_multi_metrics_constraints(
    column_name: str, column_profile: ColumnProfileView
) -> List[MetricConstraint]:
    constraints = []
    if is_probably_unique(column_profile) and not only_null_values(column_profile):
        constraints.append(column_is_probably_unique(column_name))
    return constraints
