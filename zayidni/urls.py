from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # API namespaces
    path('api/users/', include('users.urls')),
    path('api/listings/', include('listings.urls')),
    path('api/bids/', include('bids.urls')),
    path('api/payments/', include('payments.urls')),
]
