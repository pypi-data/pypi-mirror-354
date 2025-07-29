from typing import List, Union

from gencrafter.core.stubs import np as np
from gencrafter.core.stubs import pd as pd

COMMON_COLUMNAR_TYPES = Union[pd.Series, np.ndarray, List]
LARGE_CACHE_SIZE_LIMIT = 1024 * 100
