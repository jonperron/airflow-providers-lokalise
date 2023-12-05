"""
Unittest module to test Hook

Requires the unittest, pytest and requests-mock Python libraries

Run test:
    python3 -m unittest tests.hooks.test_lokalise_hook.TestLokaliseHook
"""

import logging
import pytest
from unittest.mock import Mock, patch

from airflow.models import Connection
from airflow.utils import db
from lokalise import Client as LokaliseClient
from lokalise.models.project import ProjectModel
from lokalise.errors import Unauthorized


from lokalise_provider.hooks.lokalise import LokaliseHook

log = logging.getLogger(__name__)

pytestmark = pytest.mark.db_test

lokalise_client_mock = Mock(name="lokalise_client_for_test")


class TestLokaliseHook:
    def setup_class(self) -> None:
        db.merge_conn(
            Connection(
                conn_id="lokalise_default",
                conn_type="lokalise",
                password="my-super-token",
                host="default_project",
            )
        )

    @patch(
        "lokalise_provider.hooks.lokalise.LokaliseClient",
        autospec=True,
        return_value=lokalise_client_mock,
    )
    def test_lokalise_client_connection(self, lokalise_mock) -> None:
        lokalise_hook = LokaliseHook()

        assert lokalise_mock.called
        assert isinstance(lokalise_hook.client, Mock)
        assert lokalise_hook.client.name == lokalise_mock.return_value.name

    def test_connection_success(self) -> None:
        hook = LokaliseHook()
        hook.client = Mock(spec=LokaliseClient)
        hook.client.project.return_value = ProjectModel

        status, msg = hook.test_connection()

        assert status is True
        assert msg == "Successfully connected to Lokalise."

    def test_connection_failure(self) -> None:
        hook = LokaliseHook()
        hook.client.project = Mock(
            side_effect=Unauthorized(code=401, msg="API token is incorrect")
        )

        status, msg = hook.test_connection()

        assert status is False
        assert msg == "('API token is incorrect', 401)"
