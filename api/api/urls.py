from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/staff/', include('staff.urls')),
    path('api/students/', include('students.urls')),
    path('api/', include('gradebook.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
