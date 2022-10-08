from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
import os
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("APPNAME.urls")),
    path('tinymce/', include('tinymce.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
	]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns.append(path('api-auth/', include('rest_framework.urls')))

# urlpatterns.append(path("unicorn/", include("django_unicorn.urls")))
# urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js'
TINYMCE_COMPRESSOR = False