import factory

from restaurant.models import Menu, Category, MenuItem


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    title = factory.Sequence(lambda n: f"test_menu_{n}")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: f"test_cat_{n}")
    slug = factory.Faker("slug")


class MenuItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MenuItem

    title = factory.Sequence(lambda n: f"test_menu_{n}")
    category = factory.SubFactory(CategoryFactory)
    menu = factory.SubFactory(MenuFactory)
    price = 100
    featured = True
