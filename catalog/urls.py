from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index_con, CategoryListView, ProductListView, HomeTemplateView, ProductCreateView, \
    ProductDetailView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('contacts/', index_con, name='contacts'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/products', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='view_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product')
]
