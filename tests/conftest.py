import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import MenuFactory

register(MenuFactory)


# will be available globally
@pytest.fixture
def api_client():
    return APIClient
