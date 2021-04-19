from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.datetime_safe import strftime

from .constants import DEAL_STAGES, PREFERRED_METHOD_OF_CONTACT
from .validators import mobile_number_validator, discount_validator

User = get_user_model()


class Customer(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now=True)
    date_to_be_contacted = models.DateField(editable=False)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    mobile_number = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        validators=[mobile_number_validator, ]
    )
    email = models.EmailField(null=True, blank=True)
    contact_method = models.CharField(
        choices=PREFERRED_METHOD_OF_CONTACT,
        max_length=50,
        null=True, blank=True
    )
    pdpa_agreed = models.BooleanField(
        help_text='Customer has agreed to PDPA rules.',
        verbose_name = 'PDPA Acknowledged'
    )
    deal_stage = models.CharField(
        max_length=50,
        choices=DEAL_STAGES,
        null=True,
        blank=True,
    )
    comments = models.TextField(null=True, blank=True)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def date_to_be_contacted(self):
        return self.date_created + timedelta(days=7)

    def __str__(self):
        return self.get_full_name


class Location(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Sale(models.Model):
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField('Product', related_name='sale')
    discount = models.PositiveSmallIntegerField(default=0, validators=[discount_validator, ])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    invoice_total = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.date.strftime('%d %b %y')}"


class Product(models.Model):
    name = models.CharField(max_length=55)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    url = models.URLField(null=True, blank=True)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_free:
            self.price = 0.00
        super().save(*args, **kwargs)
