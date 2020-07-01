from django.db import models

# Create your models here.

class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now_add=True)
    restatur = models.CharField(max_length=30,default="0")

    class Meta:
        abstract = True

class BookUser(BaseModel):
    username = models.CharField(max_length=256)
    password =  models.CharField(max_length=64)
    maill =  models.CharField(max_length=128)
    tel =  models.CharField(max_length=128)

    class Meta:
        db_table = "drf_book_user"