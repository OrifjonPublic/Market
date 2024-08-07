from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from category.models import Category
from base.models import BaseModel
from account.models import MyUser


class Store(BaseModel):
    name = models.CharField(_("Store Name"), max_length=200)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_stores")
    address = models.CharField(_("Address"), max_length=200)
    phone_number = models.CharField(_("Phone Number"), max_length=20)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
    
    def __str__(self):
        return self.name + " - " + self.owner.phone_number


class Product(BaseModel):
    name = models.CharField(_("product name"), max_length=200)
    description = models.TextField(_("description"), null=True, blank=True)
    price = models.DecimalField(_("product Price"), max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_products")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            num=90100 + self.id
            self.slug = f"{slugify(self.name)}-{num}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

