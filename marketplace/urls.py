from django.urls import path
from rest_framework.routers import SimpleRouter

from marketplace import views
from marketplace.views import CategoryViewSet, ProductViewSet

urlpatterns = [
    path('bucket/', views.bucket_total),
    path('bucket/add', views.bucketproduct_add),
    path('bucket/<int:pk>/update', views.product_update),
    path('bucket/<int:pk>', views.product_delete),
    path('create-order', views.create_order),

]
router = SimpleRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'product', ProductViewSet, basename='product')




urlpatterns = urlpatterns+ router.urls
