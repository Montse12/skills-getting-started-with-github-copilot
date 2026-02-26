import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(scope="session")
def client():
    """Provide a TestClient instance for the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities():
    """Reset the in-memory activities dictionary before each test.

    Because the global `activities` object in ``src.app`` is modified by
    signup and delete operations, tests could otherwise interfere with one
    another. This fixture copies the original structure and then restores it
    after the test finishes, ensuring a fresh start each time.
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original
