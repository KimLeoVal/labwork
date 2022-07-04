from django.urls import path

from webapp.views import index_view, product_view, create_product, update_product, delete_product

urlpatterns = [
    path('', index_view, name='index_view'),
    path('product/<pk>', product_view, name='product_view'),
    path('create/', create_product, name='create_product'),
    path('product/<pk>/update/', update_product, name='update_product'),
    path('product/<pk>/delete/', delete_product, name='delete_product'),

]
