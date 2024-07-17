from django.db import models

class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(default=5)

    class Meta:
        verbose_name = 'Menu'

    def __str__(self) -> str:
        return f'{self.title}'

class Booking(models.Model):
    name = models.CharField(max_length=255)
    number_of_guests = models.IntegerField(default=2)
    booking_date =models.DateTimeField()

    class Meta:
        verbose_name = 'Booking'

    def __str__(self) -> str:
        return f'{self.name}'