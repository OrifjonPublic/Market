from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from base.models import BaseModel


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError("Phone number must be provided")
        
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    GENDER = (
        ("Male", _("Male")),
        ("Female", _("Female"))
    )
    email = models.EmailField(_("Email"), unique=True, null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), unique=True, max_length=20, null=True, blank=True)
    first_name = models.CharField(_("First Name"), max_length=30, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=30, null=True, blank=True)
    middle_name = models.CharField(_("Middle Name"), max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    gender = models.CharField(_("Gender"), choices=GENDER, max_length=10, null=True, blank=True)
    address = models.TextField(_("Address"), null=True, blank=True)
    username = models.CharField(_("username"), max_length=150, null=True, blank=True )
    is_active = models.BooleanField(_("active"), default=False)

    USERNAME_FIELD = "phone_number"
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

def check_kod(kod):
    if len(str(kod))!=5:
        raise ValidationError("Kod 5 ta raqamdan iborat bolishi kerak")

class Tasqidlash(BaseModel):
    code = models.PositiveIntegerField(_('Verification code'), validators=[check_kod])
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_kodi")
    is_active = models.BooleanField(_("Active"), default=True)

    def __str__(self) -> str:
        return self.user.phone_number + " - " + str(self.code)  

    class Meta:
        verbose_name = _("Tasdiqlash")
        verbose_name_plural = _("Tasdiqlashlar")

