from django.urls import path,include
import xadmin
from xadmin.plugins import xversion
from django.views import static
from django.conf import settings, urls

xversion.register_models()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('home/', include("home.urls")),
    path('user/', include("user.urls")),
    # 设置media路由
    urls.url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
]
