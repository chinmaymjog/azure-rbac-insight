"""Exercise dashboard filters with local CSV fixtures, without Azure access."""

import io
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"
CSV = """Subscription,RoleDefinitionName,ObjectType,ObjectId,Scope
Production,Reader,User,one,/subscriptions/production
,Owner,Group,two,/subscriptions/production
Production,,ServicePrincipal,three,/subscriptions/production
Production,Reader,,four,/subscriptions/production
,,User,five,/subscriptions/production
"""


def run_dashboard(csv=CSV):
    data = pd.read_csv(io.StringIO(csv))
    app = AppTest.from_file(str(APP))
    # This is the same session-state handoff used by both ingestion paths.
    app.session_state["df"] = data
    with patch("azure.mgmt.subscription.SubscriptionClient") as client:
        client.return_value.subscriptions.list.return_value = []
        app.run(timeout=20)
    if not app.exception:
        app.sidebar.radio[0].set_value("CSV Upload (Offline)").run(timeout=20)
    return app, data


def test_blank_filter_cells_remain_visible_by_default():
    app, original = run_dashboard()
    assert not app.exception
    assert app.sidebar.multiselect[0].options == ["Production", "Unknown"]
    assert app.sidebar.multiselect[1].options == ["Owner", "Reader", "Unknown"]
    assert app.sidebar.multiselect[2].options == ["Group", "ServicePrincipal", "Unknown", "User"]
    assert app.metric[0].value == "5"
    displayed = app.dataframe[0].value
    assert len(displayed) == 5
    assert displayed.loc[1, "Subscription"] == "Unknown"
    assert displayed.loc[2, "RoleDefinitionName"] == "Unknown"
    assert displayed.loc[3, "ObjectType"] == "Unknown"
    # Preparing display labels must not overwrite the ingested data.
    assert pd.isna(original.loc[1, "Subscription"])
    pd.testing.assert_frame_equal(app.session_state["df"], original)


@pytest.mark.parametrize("index, expected_count", [(0, "2"), (1, "2"), (2, "1")])
def test_unknown_can_be_selected_without_losing_rows(index, expected_count):
    app, _ = run_dashboard()
    assert not app.exception
    app.sidebar.multiselect[index].set_value(["Unknown"]).run(timeout=20)
    assert not app.exception
    assert app.metric[0].value == expected_count


@pytest.mark.parametrize("index", [0, 1, 2])
def test_clearing_a_filter_shows_no_assignments(index):
    app, _ = run_dashboard()
    assert not app.exception
    app.sidebar.multiselect[index].set_value([]).run(timeout=20)
    assert not app.exception
    assert app.metric[0].value == "0"


def test_existing_complete_data_still_renders():
    app, _ = run_dashboard(
        "Subscription,RoleDefinitionName,ObjectType,ObjectId\nProduction,Reader,User,one\n"
    )
    assert not app.exception
    assert app.metric[0].value == "1"
    assert app.sidebar.multiselect[0].options == ["Production"]


def test_subscription_failure_is_not_cached():
    st_cache = pytest.importorskip("streamlit").cache_data
    st_cache.clear()
    calls = {"n": 0}

    def fake_client(_cred):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("not logged in")
        sub = type("S", (), {"display_name": "Prod", "subscription_id": "abc"})()
        client = type("C", (), {})()
        client.subscriptions = type("L", (), {"list": staticmethod(lambda: [sub])})()
        return client

    with patch("azure.mgmt.subscription.SubscriptionClient", fake_client), \
         patch("azure.identity.DefaultAzureCredential"):
        app = AppTest.from_file(str(APP)).run(timeout=20)
        assert not app.exception
        assert app.sidebar.error  # first run surfaces the failure
        app.run(timeout=20)  # after "az login": must retry, not reuse a cached {}
        assert not app.exception
        assert app.sidebar.multiselect[0].options == ["Prod"]
    st_cache.clear()


def test_reset_clears_cache_data():
    data = pd.read_csv(io.StringIO(CSV))
    app = AppTest.from_file(str(APP))
    app.session_state["df"] = data
    with patch("azure.mgmt.subscription.SubscriptionClient") as client, \
         patch("streamlit.cache_data.clear") as clear:
        client.return_value.subscriptions.list.return_value = []
        app.run(timeout=20)
        next(b for b in app.button if b.label == "Clear Cache / Reset").click().run(timeout=20)
    clear.assert_called()
