from django.db import models
from .validators import mobile_number_validator, discount_validator


class Customer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    mobile_number = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        validators=[mobile_number_validator, ]
    )
    email = models.EmailField(null=True, blank=True)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name


class Location(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Sale(models.Model):
    date = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField('Product', related_name='sale')
    discount = models.PositiveSmallIntegerField(default=0, validators=[discount_validator, ])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    invoice_total = models.DecimalField(default=0, decimal_places=2)

    def __str__(self):
        return self.date


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2)
    url = models.URLField(null=True, blank=True)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_free:
            self.price = 0.00
        super().save(*args, **kwargs)
