import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError, Error
from decimal import Decimal
from restaurant.models import Menu, Category, MenuItem, Order, User, OrderItem, Cart

# import factories from previous directory
from ..factories import (
    MenuItemFactory,
    CategoryFactory,
    MenuFactory,
    OrderFactory,
    CartFactory,
)


pytestmark = pytest.mark.django_db


class TestMenuModel:
    test_name = "menu123"

    def test_obj(self):
        MenuFactory(title=self.test_name)

    def test_title_unique_field(self):
        MenuFactory(title=self.test_name)
        with pytest.raises(IntegrityError):
            MenuFactory(title=self.test_name)

    def test_str_output(self):
        obj = MenuFactory(title=self.test_name)
        assert obj.__str__() == self.test_name


class TestMenuItemModel:
    def test_obj(self):
        MenuItemFactory(title="Vvvvv")

    def test_name_max_length(self):
        title = "x" * 256
        obj = MenuItemFactory.build(title=title)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_foreign_key_relationships(self):
        menu_item = MenuItemFactory.create()
        category = menu_item.category
        menu = menu_item.menu

        assert isinstance(category, Category)
        assert isinstance(menu, Menu)

        assert category.pk is not None
        assert menu.pk is not None
        assert menu_item.category_id == category.id
        assert menu_item.menu_id == menu.id


class TestCategoryModel:
    test_title = "cat123"
    test_slug = "slug123"

    def test_obj(self):
        CategoryFactory(title=self.test_title, slug=self.test_slug)

    def test_title_unique_field(self):
        CategoryFactory(title=self.test_title)
        with pytest.raises(IntegrityError):
            CategoryFactory(title=self.test_title)

    def test_str_output(self):
        obj = CategoryFactory(title=self.test_title, slug=self.test_slug)
        assert obj.__str__() == self.test_title


class TestOrderModel:
    def test_obj(self):
        OrderFactory()

    def test_total_field_max_digits_and_decimal_places(self):
        valid_total = Decimal("1234.56")
        order = OrderFactory(total=valid_total)
        assert order.total == valid_total

        too_large_total = Decimal("12345.67")
        order = OrderFactory.build(total=too_large_total)
        with pytest.raises(ValidationError):
            order.full_clean()

    def test_str_output(self):
        obj = OrderFactory()
        assert obj.__str__() == f"{obj.id} - User: {obj.user.username} Order: {obj.id}"

    def test_foreign_key_relationships(self):
        obj = OrderFactory()
        user = obj.user
        delivery_crew = obj.delivery_crew

        assert isinstance(user, User)
        assert isinstance(delivery_crew, User)

        assert obj.user_id == user.id
        assert obj.delivery_crew_id == delivery_crew.id


class TestCartModel:
    def test_obj(self):
        CartFactory()

    def test_str_output(self):
        obj = CartFactory()
        assert f"{obj.user.email}"

    def test_foreign_key_relationships(self):
        obj = CartFactory()
        user = obj.user
        order = obj.order

        assert isinstance(user, User)
        assert isinstance(order, Order)

        assert obj.user_id == user.id
        assert obj.order_id == order.id
