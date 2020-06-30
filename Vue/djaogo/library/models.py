from django.db import models

# Create your models here.

class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Book(BaseModel):
    book_name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to="pic",default="")
    publisher = models.ForeignKey(to="Publish",on_delete=models.CASCADE,
                            db_constraint=False,related_name="books")
    class Meta:
        db_table = "drf_book"

class Publish(BaseModel):
    publish = models.CharField(max_length=256)
    img = models.ImageField(upload_to="pic",default="")
    address = models.CharField(max_length=256)

    class Meta:
        db_table = "drf_publisher"
        verbose_name = "出版商"
        verbose_name_plural = verbose_name