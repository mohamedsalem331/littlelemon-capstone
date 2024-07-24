import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from restaurant.models import Menu

pytestmark = pytest.mark.django_db


class TestMenuModel:
    def test_title_unique_field(self, menu_factory):
        menu_factory(title="test_title")
