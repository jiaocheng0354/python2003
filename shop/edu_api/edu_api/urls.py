from django.urls import path, include
import xadmin
from xadmin.plugins import xversion
from django.views import static
from django.conf import settings, urls

xversion.register_models()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('home/', include("home.urls")),
    path('user/', include("user.urls")),
    path('course/', include("course.urls")),
    path('cart/', include("cart.urls")),
    path('order/', include("order.urls")),
    path('payments/', include("payments.urls")),
    # 富文本编辑器的路由
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # 设置media路由
    urls.url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    urls.url(r'^video/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
]
