from django.db import models
from django.utils.translation import gettext_lazy as _

from product.models import Product
from base.models import BaseModel, Photo


class Discount(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="discounts")
    discount_percent = models.PositiveIntegerField(_("Discount Percentage"), default=0)
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))
    discount_name = models.CharField(_("discount name"), max_length=250, null=True, blank=True)
    photo = models.ImageField(upload_to='discounts/', null=True, blank=True)    
    is_active = models.BooleanField(default=True)
        
    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")
        ordering = ['-start_date']
    
    def __str__(self) -> str:
        return self.discount_name + str(self.discount_percent) + "% - " + str(self.product)


