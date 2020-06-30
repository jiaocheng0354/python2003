from django.db import models

# Create your models here.
class Stu(models.Model):
    username = models.CharField(max_length=80)
    age = models.SmallIntegerField()
    password = models.CharField(max_length=64)
    grade = models.CharField(max_length=10)
    stuNumber = models.CharField(max_length=40)

    class Meta:
        db_table = "drf_stu"
