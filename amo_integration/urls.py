
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('amo/', include('amo.urls')),
    path('ticket/', include('ticket.urls')),
]
