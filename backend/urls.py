from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from backend.user.views import health_check


urlpatterns = [
    path("health/", health_check, name="health"),  # Add this
    path("admin/", admin.site.urls),
    path("api/v1/", include("backend.task.urls")),
    path("api/v1/", include("backend.user.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
