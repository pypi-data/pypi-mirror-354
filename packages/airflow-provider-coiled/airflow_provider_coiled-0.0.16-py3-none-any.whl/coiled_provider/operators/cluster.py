from typing import TYPE_CHECKING, Callable
from airflow.sdk.bases.decorator import task_decorator_factory
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.decorators.base import DecoratedOperator
from airflow.sdk.bases.decorator import TaskDecorator


class CoiledClusterOperator(PythonOperator):
    def __init__(self, python_callable: Callable, **kwargs):
        # requirements = [
        #     "coiled",
        #     "dask[complete]",
        #     "tornado==6.4.2",
        #     "pandas==2.1.4",
        #     "numpy==1.26.4",
        #     "geopandas",
        #     "dask_geopandas",
        #     "s3fs",
        #     "pyarrow",
        #     "matplotlib",
        # ]
        # index_urls = ["https://pypi.org/simple"]
        super().__init__(
            # requirements=requirements,
            # index_urls=index_urls,
            python_callable=python_callable,
            **kwargs,
        )

    def execute(self, context):
        super().execute(context=context)


class _CoiledClusterDecoratedOperator(DecoratedOperator, CoiledClusterOperator):
    custom_operator_name = "@task.coiled_cluster"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def coiled_cluster_task(
    python_callable: Callable | None = None,
    multiple_outputs: bool | None = None,
    **kwargs,
) -> TaskDecorator:
    """
    Wrap a callable into an Airflow operator to run via a Python virtual environment.

    Accepts kwargs for operator kwarg. Can be reused in a single DAG.

    This function is only used only used during type checking or auto-completion.

    :meta private:

    :param python_callable: Function to decorate
    :param multiple_outputs: If set to True, the decorated function's return value will be unrolled to
        multiple XCom values. Dict will unroll to XCom values with its keys as XCom keys.
        Defaults to False.
    """

    return task_decorator_factory(
        python_callable=python_callable,
        multiple_outputs=multiple_outputs,
        decorated_operator_class=_CoiledClusterDecoratedOperator,
        **kwargs,
    )
