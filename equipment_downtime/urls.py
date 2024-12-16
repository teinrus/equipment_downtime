from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('settings/', include('settings_app.urls')),
    path('', include('downtime.urls')),
]
