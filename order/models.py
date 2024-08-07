from typing import Iterable
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from product.models import Product
from base.models import BaseModel
from account.models import MyUser


class SelectedProduct(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="my_selected_products")
    total_price = models.DecimalField(_("total price"))
    
    def save(self, *a, **b) -> None:
        if self.quantity < 1:
            raise ValidationError(_("Mahsulot tanlanmagan, kamida 1 ta tanlanishi kerak."))
        self.total_price = self.product.price * self.quantity
        super().save(*a, **b)

    class Meta:
        verbose_name = _("Selected Product")
        verbose_name_plural = _("Selected Products")
    