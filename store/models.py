from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    # def get_absolute_url(self):
    #     return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=255, default="admin")
    image = models.ImageField(upload_to="images/")
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_creator"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_category"
    )

    class Meta:
        verbose_name_plural = "products"
        ordering = ["-created"]

    def __str__(self):
        return self.title