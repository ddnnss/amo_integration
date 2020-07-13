
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = ""
admin.site.site_title = ""
admin.site.index_title = ""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('amo/', include('amo.urls')),
    path('ticket/', include('ticket.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
