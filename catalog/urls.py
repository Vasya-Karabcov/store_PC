from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, index_con, index_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', index_con, name='contacts'),
    path('product/', index_product, name='product')
]
