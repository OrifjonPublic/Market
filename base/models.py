from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Photo(BaseModel):
    photo = models.ImageField(upload_to='photos/')


class Company(BaseModel):
    name = models.CharField(max_length=300)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.name


class CompanyLogo(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="logo_photo")
    logo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)  
    
    class Meta:
        verbose_name_plural = "Company Logos"
        verbose_name = 'Company Logo'  

class CompanySocialLinks(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='social_link_images')
    url = models.URLField()
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='social_links')
    
    class Meta:
        verbose_name_plural = "Company Social Links"
        verbose_name = 'Company Social Link'


