from typing import TYPE_CHECKING, Callable
from airflow.sdk.bases.decorator import task_decorator_factory
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.decorators.base import DecoratedOperator
from airflow.sdk.bases.decorator import TaskDecorator


class CoiledClusterOperator(PythonOperator):
    # def __init__(self, python_callable: Callable, **kwargs):
    #     # requirements = [
    #     #     "coiled",
    #     #     "dask[complete]",
    #     #     "tornado==6.4.2",
    #     #     "pandas==2.1.4",
    #     #     "numpy==1.26.4",
    #     #     "geopandas",
    #     #     "dask_geopandas",
    #     #     "s3fs",
    #     #     "pyarrow",
    #     #     "matplotlib",
    #     # ]
    #     # index_urls = ["https://pypi.org/simple"]
    #     super().__init__(
    #         # requirements=requirements,
    #         # index_urls=index_urls,
    #         python_callable=python_callable,
    #         **kwargs,
    #     )

    def execute(self, context):
        super().execute(context=context)


class _CoiledClusterDecoratedOperator(DecoratedOperator, CoiledClusterOperator):
    custom_operator_name = "@task.coiled_cluster"


def coiled_cluster_task(
    python_callable: Callable | None = None,
    multiple_outputs: bool | None = None,
    **kwargs,
) -> TaskDecorator:
    return task_decorator_factory(
        python_callable=python_callable,
        multiple_outputs=multiple_outputs,
        decorated_operator_class=_CoiledClusterDecoratedOperator,
        **kwargs,
    )
