from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index_con, CategoryListView, ProductListView, HomeTemplateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('contacts/', index_con, name='contacts'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/products', ProductListView.as_view(), name='product_list'),
]
