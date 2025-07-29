__version__ = "1.0.0"

# This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.


def get_provider_info():
    return {
        "package-name": "airflow-provider-coiled",  # Required
        "name": "Sample",  # Required
        "description": "An airflow provider for coiled",  # Required
        "versions": [__version__],  # Required
        "task-decorators": [
            {
                "name": "coiled_cluster",
                # "Import path" and function name of the `foo_task`
                "class-name": "coiled_provider.operators.coiled_cluster_task",
            }
        ],
        # "connection-types": [
        #     {
        #         "connection-type": "sample",
        #         "hook-class-name": "sample_provider.hooks.sample.SampleHook",
        #     }
        # ],
        # "extra-links": ["sample_provider.operators.sample.SampleOperatorExtraLink"],
    }
