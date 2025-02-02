# LBA/urls.py

from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse

def service_worker(request):
    return HttpResponse(status=204)

# Non-translated URLs - keep only the basic patterns here
urlpatterns = [
    path('serviceworker.js', service_worker),
    path('i18n/', include('django.conf.urls.i18n')),  # Language switching URLs
]

# Add translated URLs
urlpatterns += i18n_patterns(
    path('', include('b11_1.urls')),  # Include all your app URLs
    path('main_admin/', admin.site.urls),
    prefix_default_language=True
)

# Add static/media patterns at the end
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
