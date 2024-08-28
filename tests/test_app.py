"""A suite of unit tests for the streamlit app in the base directory. We encourage
adding tests into this suite to ensure functionality within your streamlit app, particularly
for the components that allow users to interact with the app (buttons, dropdown menus, etc).

These tests were all written using Streamlit's AppTest class. See here for more details:
https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest#run-an-apptest-script

A few considerations:

1. This suite is meant to be run from the base directory, not from the tests directory.
2. The streamlit app is meant to be run from the base directory.
3. The streamlit app is assumed to be called ``app.py``.
"""

import os
import sys

import pytest
from streamlit.testing.v1 import AppTest

# Ensure that the base directory is in PYTHONPATH so ``toolkit`` and other tools can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# The timeout limit to wait for the app to load before shutdown ( in seconds )
DEFAULT_TIMEOUT = 30


@pytest.fixture(scope="module")
def app():
    return AppTest.from_file(
        "app.py", default_timeout=DEFAULT_TIMEOUT
    ).run()

def test_selectbox(app):
    """Ensure that the correct selections are available from the selectbox."""

    selectbox_options = app.selectbox[0].options

    assert set(selectbox_options) == set(["Dataframe", "Line plot", "Bar plot"]), f"Incorrect selectbox options. Got {set(selectbox_options)}."

def test_outputs(app):
    """Ensure that the selectbox selections return outputs."""

    # get selectbox options
    selectbox_options = app.selectbox[0].options

    for option in selectbox_options:
        output = app.selectbox[0].set_value(option).run()
        assert output is not None