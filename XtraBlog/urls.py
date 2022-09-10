from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404

admin.site.site_title = "XtraBlog Admin"
admin.site.site_header = "XTRABLOG ADMIN"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Blog.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = 'Blog.views.error404'
handler500 =  'Blog.views.serverError'