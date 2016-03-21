from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from website import views
from website.views import GuestLogin, MenuHome, CategoryProductsList, MealForm, CreateAcct, Checkout
from .forms import CreateAccountForm


#LOGIN_REDIRECT_URL = 'website:menu'

urlpatterns = [
    url(r'^$', views.index, name="index"),

    # Vistas autogeneradas
    url(r'^login/$', auth_views.login, 
        {'template_name': 'website/wizard/login.html'}, name='login-auth'),
    
    url(r'^login/guest/$', GuestLogin.as_view(), name="guest-login"),
    url(r'^signup/$', views.CreateAcct.as_view(), name="new-account"),
    url(r'^logout/$', views.userLogout, name="userlogout"),

    # Vistas del Menu
    url(r'^menu/$', views.MenuHome.as_view(), name="menu"),
    url(r'^menu/category/(?P<pk>[0-9]+)/$', views.CategoryProductsList.as_view(), name="ProductList"),
    url(r'^menu/category/(?P<pk_cat>[0-9]+)/product/(?P<pk_prod>[0-9]+)/$', views.MealForm.as_view(), name="MealForm"),
    url(r'^menu/checkout/type$', views.pre_checkout, name="pre_checkout"),
    url(r'^menu/checkout/payment$', 
        login_required(views.Checkout.as_view()), name="checkout"),

    #url(r'^menu/checkout/payment$', views.checkout, name="checkout"),
    url(r'^menu/checkout/thankyou/$', views.thankyou, name="thankyou"),
    #url(r'^menu/view-cart/$', views.ViewCart, name="view-cart"),
    url(r'^menu/view-cart/delete-item/(?P<item>[0-9]+)/$', views.DeleteItem, name="delete-item"),
    #url(r'^menu/order-history/$', views.OrderHistory, name="order-history"),
    url(r'^menu/empty-cart/$', views.empty_cart, name="empty_cart"),
    url(r'^menu/closed/$', views.closed, name="closed"),
]