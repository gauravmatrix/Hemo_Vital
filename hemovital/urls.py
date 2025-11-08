from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Django Admin Panel
    path('admin/', admin.site.urls),
    
    # 2. Core App URLs
    # Yeh line poore project ke sabhi URLs (homepage, login, register, dashboards, etc.)
    # ko 'core' app ko handle karne ke liye bhej degi.
    path('', include('core.urls')),
]

# Yeh media files (jaise profile photos, hospital logos) ko development server par
# dikhane ke liye bahut zaroori hai.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

