from django.urls import path

from catalog.views import index, index_con, index_product

urlpatterns = [
    path('', index),
    path('contacts/', index_con),
    path('product/', index_product)
]
