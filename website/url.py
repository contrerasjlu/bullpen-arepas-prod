from django.conf.urls import url
from website import views

urlpatterns = [
    url(r'^home/$', views.index, name="index"),
    url(r'^menu/$', views.menu, name="menu"),
    url(r'^menu/product/(?P<id_for_prod>[0-9]+)/$', views.ProductDetail, name="product_detail"),
    url(r'^menu/closed/$', views.closed, name="closed"),
]