from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index_con, CategoryListView, ProductListView, HomeTemplateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='index'),
    path('contacts/', index_con, name='contacts'),
    path('product/', CategoryListView.as_view(), name='product_list'),
    path('product_pr/<int:pk>/', ProductListView.as_view(), name='product_pr_list'),
    path('product_mp/', ProductListView.as_view(), name='product_mp_list'),
    path('product_op/', ProductListView.as_view(), name='product_op_list'),
    path('product_bp/', ProductListView.as_view(), name='product_bp_list'),
]
