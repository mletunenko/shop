from django.urls import path
from marketplace import views

urlpatterns = [
    path('category/', views.category_list),
    path('category/<int:pk>/', views.category_detail),
    path('product/', views.product_list),
    path('product/<int:pk>/', views.product_detail),
    path('bucket/', views.bucket_total),
    path('bucket/add', views.bucketproduct_add),
    path('bucket/<int:pk>/update', views.product_update),
    path('bucket/<int:pk>', views.product_delete),
]