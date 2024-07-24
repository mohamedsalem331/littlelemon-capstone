import factory

from restaurant.models import Menu


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    title = factory.Sequence(lambda n: f"test_menu_{n}")
