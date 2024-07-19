from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class ExtendedManager(models.Manager):
    def by_user(self, id):
        return self.filter(creatorId=id)


class CommonInfo(models.Model):
    creatorId = models.IntegerField(default=0)
    objects = ExtendedManager()

    class Meta:
        abstract = True


class Menu(CommonInfo):
    title = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    inventory = models.IntegerField(default=5)

    class Meta:
        verbose_name = "Menu"

    def __str__(self) -> str:
        return f"{self.title}"


class Booking(CommonInfo):
    name = models.CharField(max_length=255)
    number_of_guests = models.IntegerField(default=2, max=10)
    booking_date = models.DateTimeField()

    def clean(self):
        super().clean()  # Call the parent class's clean method
        if self.booking_date <= timezone.now():
            raise ValidationError("Booking date must be in the future.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure the clean method is called before saving
        super(Booking, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Booking"

    def __str__(self) -> str:
        return f"{self.name}"
