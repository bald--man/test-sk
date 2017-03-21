from django.conf.urls import url
from django.contrib import admin

from .views import (
    product_list,
    product_detail,
    product_update,
    product_create,
    ProductLikeToggle,
    )

urlpatterns = [
    url(r'^$', product_list, name='list'),
    url(r'^create/$', product_create),
    url(r'^(?P<slug>[\w-]+)/$', product_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/like/$', ProductLikeToggle.as_view(), name='like-toggle'),
    url(r'^(?P<slug>[\w-]+)/edit/$', product_update, name='update'),
]
