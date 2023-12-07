__version__ = "1.0.1"

## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-provider-lokalise",  # Required
        "name": "Lokalise",  # Required
        "description": "Lokalise hook and operator for Airflow based on the Lokalise Python SDK.",  # Required
        "connection-types": [
            {
                "connection-type": "lokalise",
                "hook-class-name": "airflow-provider-lokalise.hooks.lokalise.LokaliseHook",
            }
        ],
        "extra-links": [
            "airflow-provider-lokalise.operators.lokalise.LokaliseOperator"
        ],
        "versions": [__version__],  # Required
    }
