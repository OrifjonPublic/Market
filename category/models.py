from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from base.models import Photo
from product.models import Product


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
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(_("Attribute Name"), max_length=100)
    

class AttributeValue(models.Model):
    attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(_("Value"), max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_values")

    class Meta:
        verbose_name = 'Attribute Value'
        verbose_name_plural = 'Attribute Values'

