from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    thumbnail_url = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    stock = models.BooleanField(default=False, blank=True)
    product_description = models.CharField(max_length=200, blank=True)
    upc = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.title
