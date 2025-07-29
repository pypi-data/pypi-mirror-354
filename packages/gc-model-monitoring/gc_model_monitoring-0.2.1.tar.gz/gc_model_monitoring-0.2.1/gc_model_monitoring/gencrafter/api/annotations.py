from types import FunctionType, LambdaType, MethodType
from typing import Optional, Union

from gencrafter.api.logger import log
from gencrafter.core import DatasetSchema

FuncType = Union[FunctionType, MethodType, LambdaType]


def profiling(*, schema: Optional[DatasetSchema] = None):  # type: ignore
    def decorated(func: FuncType) -> FunctionType:
        def wrapper(*args, **kwargs):  # type: ignore
            df = func(*args, **kwargs)
            df.profiling_results = log(pandas=df, schema=schema)
            return df

        return wrapper  # type: ignore

    return decorated
