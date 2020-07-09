from django.db import models

from home.BaseModel import BaseModel


class Banner(BaseModel):
    img = models.ImageField(upload_to="banner", max_length=225, verbose_name="图片")
    title = models.CharField(max_length=225, verbose_name="标题")
    link = models.CharField(max_length=225, verbose_name="链接")

    class Meta:
        db_table = "shop_banner"
        verbose_name = "广告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Nav(BaseModel):
    """导航栏"""
    POSITION_OPTION = (
        (1, "顶部"),
        (2, "底部"),
    )
    title = models.CharField(max_length=200, verbose_name="标题")
    link = models.CharField(max_length=300, verbose_name="链接")
    position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name="位置")
    is_site = models.BooleanField(default=False, verbose_name="是否是外部链接")

    class Meta:
        db_table = "shop_nav"
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

