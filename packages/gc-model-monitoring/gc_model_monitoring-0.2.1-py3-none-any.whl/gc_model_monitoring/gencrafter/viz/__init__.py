import IPython  # type: ignore  # noqa  # import ipython to make

from gencrafter.viz.extensions.reports.summary_drift import SummaryDriftReport
from gencrafter.viz.notebook_profile_viz import NotebookProfileVisualizer

__ALL__ = [
    # column
    NotebookProfileVisualizer,
    SummaryDriftReport,
]
