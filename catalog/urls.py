from django.urls import path

from catalog.views import index, index_con

urlpatterns = [
    path('', index),
    path('contacts/', index_con)
]
