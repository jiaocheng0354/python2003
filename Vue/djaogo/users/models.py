from django.db import models

# Create your models here.
class User(models.Model):
    gender_choices = (
        (0,"male"),
        (1,"female"),
        (2,"other"),
    )
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=64)
    gender = models.SmallIntegerField(choices=gender_choices,default=0)

    class Meta:
        db_table = "drf_user"