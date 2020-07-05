from django.db import models


class Emp(models.Model):
    name = models.CharField(max_length=80)
    photo = models.ImageField(upload_to="pic", default="pic/1.jpg")
    salary = models.DecimalField(max_digits=4, decimal_places=2)
    age = models.IntegerField()

    class Meta:
        db_table = "ems_emp"
