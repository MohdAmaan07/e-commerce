from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('collections/', views.collection_list, name='collection_list'),
    path('products/<int:id>', views.product_detail, name='product_detail'),
    path('collections/<int:pk>', views.collection_detail, name='collection_detail'),
]
