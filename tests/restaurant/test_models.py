import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError, Error

from restaurant.models import Menu, Category, MenuItem

# import factories from previous directory
from ..factories import MenuItemFactory, CategoryFactory, MenuFactory


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
