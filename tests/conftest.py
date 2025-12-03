import pytest
from app import create_app


@pytest.fixture
def app():
    """
    Create a new app instance for each test.
    Uses the normal application factory.
    """
    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,  # disable CSRF in tests to simplify form posts
    )
    return app


@pytest.fixture
def client(app):
    """
    Flask test client for sending requests.
    """
    return app.test_client()
