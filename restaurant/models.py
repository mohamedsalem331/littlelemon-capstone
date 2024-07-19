from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class ExtendedManager(models.Manager):
    def by_user(self, id):
        return self.filter(creatorId=id)


class CommonInfo(models.Model):
    creatorId = models.IntegerField(default=0)
    objects = ExtendedManager()

    class Meta:
        abstract = True


class Category(CommonInfo):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return f"{self.title}"


class MenuItem(CommonInfo):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.title}"


class Order(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True
    )
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)


class OrderItem(CommonInfo):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("order", "menuitem")


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("menuitem", "user")

    def __str__(self):
        return f"{self.user}"


class Booking(CommonInfo):
    name = models.CharField(max_length=255)
    number_of_guests = models.IntegerField(default=2, max_length=10)
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
