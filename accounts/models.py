from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _


class UserManager(UserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(is_verified=True, *args, **kwargs)


class User(AbstractUser):
    is_verified = models.BooleanField(_('وضعیت تایید ایمیل'), default=False)
    verification_token = models.CharField(max_length=64, editable=False, blank=True, null=True)
    email = models.EmailField(_("آدرس ایمیل"), unique=True)

    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر"

    def __str__(self):
        return self.username
