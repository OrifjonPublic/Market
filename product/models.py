from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from base.models import BaseModel
from account.models import MyUser
from base.models import Photo


class Category(MPTTModel):
    name = models.CharField(_("Name"), max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True, related_name='category_photo')
    slug = models.SlugField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            num=10000 + self.id
            self.slug = f"{slugify(self.name)}-{num}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(_("Attribute Name"), max_length=100)
    

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


class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    first_name = models.CharField(_("Customer Name"), max_length=100)
    user_photo = models.ImageField(upload_to="customers/", default="user.png")
    review = models.TextField(_("Comment"))
    rate = models.PositiveIntegerField(_("Rate"))

    def __str__(self) -> str:
        return f"{self.user.phone_number}-{self.review[:50]}"
    

class AttributeValue(models.Model):
    attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(_("Value"), max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_values")

    class Meta:
        verbose_name = 'Attribute Value'
        verbose_name_plural = 'Attribute Values'
