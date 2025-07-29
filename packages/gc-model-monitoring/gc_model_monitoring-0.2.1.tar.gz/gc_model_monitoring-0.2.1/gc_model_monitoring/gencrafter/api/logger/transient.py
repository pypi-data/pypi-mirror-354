from typing import Any, Dict, List, Optional

from gencrafter.api.logger.logger import Logger
from gencrafter.core import DatasetProfile, DatasetSchema
import pandas as pd


class TransientLogger(Logger):
    def __init__(self, schema: Optional[DatasetSchema] = None):
        super(TransientLogger, self).__init__(schema)

    def _get_matching_profiles(
        self,
        obj: Any = None,
        *,
        pandas: Optional[pd.DataFrame] = None,
        row: Optional[Dict[str, Any]] = None,
        schema: Optional[DatasetSchema] = None,
    ) -> List[DatasetProfile]:
        active_schema = schema or self._schema
        return [DatasetProfile(schema=active_schema)]
