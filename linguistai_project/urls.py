from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp import admin_views

urlpatterns = [
    path('admin/dashboard/', admin_views.admin_dashboard_view, name="admin_dashboard"),
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)