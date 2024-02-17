from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from datetime import datetime
from .utils import get_username_else_email

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.TextField(null=True, blank=True)
    fb_doc_id = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "user"

    def __str__(self) -> str:
        return f"{get_username_else_email(self)},{self.id}"


class MasterProducts(models.Model):
    gender_choice = [("M", "MALE"), ("F", "FEMALE"), ("K", "KIDS")]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=500, null=False)
    price = models.FloatField(null=False)
    rating = models.FloatField(null=False)
    product_description = models.TextField(null=False)
    reviews = models.TextField(null=False)
    reviews_rating = models.TextField(null=False)
    url = models.TextField(null=False)
    size = models.FloatField(null=False)
    color = models.CharField(max_length=50, null=False)
    category = models.CharField(max_length=50, null=False)
    gender = models.CharField(
        max_length=10, null=True, blank=True, choices=gender_choice
    )

    class Meta:
        db_table = "master_products"

    def __str__(self) -> str:
        return f"{self.title},{self.id}"


class UserCart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    dateCreated = models.DateTimeField(default=datetime.now)
    product = models.ForeignKey(MasterProducts, on_delete=models.CASCADE)
    count = models.IntegerField(default=1, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "cart"

    def __str__(self) -> str:
        return f"{self.product.id} {get_username_else_email(self.user)}"


class UserOrders(models.Model):
    order_status_choices = [
        ("INITIATED", "INITIATED"),
        ("PICKED", "PICKED"),
        ("DISPATCHED", "DISPATCHED"),
        ("DELIVERED", "DELIVERED"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    dateCreated = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_ids = models.CharField(max_length=2000, null=False, blank=False)
    order_status = models.CharField(
        max_length=10,
        choices=order_status_choices,
        default="INITIATED",
    )
    order_total = models.FloatField(null=False, blank=False)

    class Meta:
        db_table = "orders"

    def __str__(self) -> str:
        return f"{self.id} {get_username_else_email(self.user)} {self.order_status}"
