import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import (
    MenuFactory,
    CategoryFactory,
    MenuItemFactory,
    UserFactory,
    CartFactory,
    OrderFactory,
    OrderItemFactory,
)

register(MenuFactory)
register(CategoryFactory)
register(MenuItemFactory)
register(UserFactory)
register(CartFactory)
register(OrderFactory)
register(OrderItemFactory)


# will be available globally
@pytest.fixture
def api_client():
    return APIClient
