from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
from airflow.models import Connection
from airflow.models.dag import DAG
from airflow.utils import db, timezone

from lokalise_provider.operators.lokalise import LokaliseOperator

pytestmark = pytest.mark.db_test

DEFAULT_DATE = timezone.datetime(2023, 12, 1)
lokalise_client_mock = Mock(name="lokalise_client_for_test")


class TestLokaliseOperator:
    def setup_class(self) -> None:
        args = {"owner": "airflow", "start_date": DEFAULT_DATE}
        dag = DAG("test_dag_id", default_args=args)
        self.dag = dag
        db.merge_conn(
            Connection(
                conn_id="lokalise_default",
                conn_type="lokalise",
                password="my-super-token",
                host="default_project",
            )
        )

    def test_operator_init_with_optional_args(self) -> None:
        lokalise_operator = LokaliseOperator(
            task_id="test_init_lokalise_list_keys", lokalise_method="keys"
        )

        assert lokalise_operator.lokalise_method_args == {}
        assert lokalise_operator.result_processor is None

    @patch(
        "lokalise_provider.hooks.lokalise.LokaliseClient",
        autospec=True,
        return_value=lokalise_client_mock,
    )
    def test_list_keys(self, lokalise_mock) -> None:
        class MockListKeys:
            pass

        keys = MockListKeys()
        keys.return_value = {"TESTING": {"en": "I AM A TEST"}}

        lokalise_mock.return_value.keys.return_value = keys

        lokalise_operator = LokaliseOperator(
            task_id="test_lokalise_list_keys",
            lokalise_method="keys",
            lokalise_method_args={
                "include_translations": 1,
                "limit": 500,
                "disable_references": 0,
                "filter_untranslated": 1,
                "filter_archived": "exclude",
            },
            result_processor=lambda r: r.__dict__,
            dag=self.dag,
        )

        lokalise_operator.run(
            start_date=DEFAULT_DATE, end_date=DEFAULT_DATE, ignore_ti_state=True
        )

        assert lokalise_mock.called
        assert lokalise_mock.return_value.keys.called
