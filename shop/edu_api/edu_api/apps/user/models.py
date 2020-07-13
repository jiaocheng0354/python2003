from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号")

    class Meta:
        db_table = "shop_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        unique_together = ["username","phone"]