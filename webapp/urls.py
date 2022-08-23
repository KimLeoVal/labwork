from django.urls import path

from webapp.views import category_view, IndexView, ProductView, CreateProduct, UpdateProduct, DeleteProduct, \
    Basket, DeleteFromBasket, CreateOrder, delete_one_by_one, AddInBasket

app_name = 'webapp'
urlpatterns = [
    path('', IndexView.as_view(), name='IndexView'),
    path('product/<int:pk>', ProductView.as_view(), name='ProductView'),
    path('create/', CreateProduct.as_view(), name='CreateProduct'),
    path('product/<int:pk>/update/', UpdateProduct.as_view(), name='UpdateProduct'),
    path('product/<int:pk>/delete/', DeleteProduct.as_view(), name='DeleteProduct'),
    path('product/cat/<str:category>', category_view, name='category_view'),
    path('proinbas/<int:pk>', AddInBasket.as_view(), name='add_in_basket'),
    path('basket/', Basket.as_view(), name='Basket'),
    path('proinbas/<int:pk>/delete/', DeleteFromBasket.as_view(), name='DeleteFromBasket'),
    path('proinbas/<int:pk>/delete1/', delete_one_by_one, name='delete_one_by_one'),
    path('order/create', CreateOrder.as_view(), name='CreateOrder'),
    # path('order/create', createorder, name='createorder'),


]
