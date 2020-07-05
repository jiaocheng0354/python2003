from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=80)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    sex = models.SmallIntegerField()

    class Meta:
        db_table = "ems_user"
        unique_together = ["username"]
