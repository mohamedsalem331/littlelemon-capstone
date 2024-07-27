import factory
import random
from restaurant.models import Menu, Category, MenuItem, Order, OrderItem, Cart, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


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


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    delivery_crew = factory.SubFactory(UserFactory)
    status = factory.LazyFunction(lambda: random.choice([True, False]))
    total = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    date = factory.Faker("date_this_year", before_today=True, after_today=False)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    menuitem = factory.SubFactory(MenuItemFactory)
    quantity = factory.Faker("random_int", min=1, max=10)


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)
    order = factory.SubFactory(OrderFactory)
