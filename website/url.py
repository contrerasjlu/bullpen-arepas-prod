from django.conf.urls import url
from website import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^home/$', views.index, name="index"),

    # Vistas autogeneradas
    url(r'^login/$', auth_views.login, {'template_name': 'website/login.html', 'extra_context':{'new_user':'CreateAccountForm()'}}),
    url(r'^signup/$', views.create_account, name="new_account"),
    url(r'^logout/$', views.userLogout, name="userlogout"),

    # Vistas del Menu
    url(r'^menu/$', views.menu, name="menu"),
    url(r'^menu/product/(?P<id_for_prod>[0-9]+)/$', views.ProductDetail, name="product_detail"),
    url(r'^menu/checkout/type$', views.pre_checkout, name="pre_checkout"),
    url(r'^menu/checkout/payment$', views.checkout, name="checkout"),
    url(r'^menu/checkout/thankyou/$', views.thankyou, name="thankyou"),
    url(r'^menu/empty-cart$', views.empty_cart, name="empty_cart"),
    url(r'^menu/closed/$', views.closed, name="closed"),
]