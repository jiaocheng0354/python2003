from django.db import models


class BaseModel(models.Model):
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        abstract = True