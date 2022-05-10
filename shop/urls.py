from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from marketplace import views, urls

router = routers.DefaultRouter()

urlpatterns = [
    path('', include('marketplace.urls')),
    path('admin/', admin.site.urls),
    # path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('marketplace_auth.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),
]
