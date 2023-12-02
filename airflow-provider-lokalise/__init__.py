from __future__ import annotations

import packaging.version

__all__ = ["__version__"]

__version__ = "8.12.0"

try:
    from airflow import __version__ as airflow_version
except ImportError:
    from airflow.version import version as airflow_version

if packaging.version.parse(packaging.version.parse(airflow_version).base_version) < packaging.version.parse(
    "2.5.0"
):
    raise RuntimeError(
        f"The package `apache-airflow-providers-amazon:{__version__}` needs Apache Airflow 2.5.0+"
    )
