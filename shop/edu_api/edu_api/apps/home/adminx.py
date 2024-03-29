import xadmin
from xadmin import views

from home.models import Banner, Nav


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "百知教育"  # 设置站点标题
    site_footer = "北京百知教育科技有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)

# 将banner注册到后台  列表显示的字段
class BannerInfo(object):
    list_display = ["title", "img", "link","is_show","is_delete","orders"]
xadmin.site.register(Banner,BannerInfo)
class NavInfo(object):
    list_display = ["title", "link", "position","is_site","is_show","is_delete","orders"]
xadmin.site.register(Nav,NavInfo)
