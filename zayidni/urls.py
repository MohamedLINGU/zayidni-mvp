from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # API namespaces
    path('api/', include('users.urls')),
    path('api/', include('listings.urls')),
    path('api/', include('bids.urls')),
]
