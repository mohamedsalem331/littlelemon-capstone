import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import MenuFactory, CategoryFactory, MenuItemFactory

register(MenuFactory)
register(CategoryFactory)
register(MenuItemFactory)


# will be available globally
@pytest.fixture
def api_client():
    return APIClient
