from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from website import views

urlpatterns = [
    url(r'^$', views.index, name="index"),

    url(r'^website/aboutus/$', views.AboutUsView.as_view(), name="AboutUsView"),

    url(r'^website/ourproducts/$', views.OurProductsView.as_view(), name="OurProductsView"),

    # Vistas autogeneradas
    url(r'^accounts/login/$', auth_views.login,
        {'template_name': 'website/wizard/login.html'}, name='login-auth'),
    
    url(r'^login/guest/$', views.GuestLogin.as_view(), name="guest-login"),
    url(r'^signup/$', views.CreateAcct.as_view(), name="new-account"),
    url(r'^logout/$', views.userLogout, name="userlogout"),

    # Configure Main
    url(r'^menu/welcome/$', views.PreCheckoutView.as_view(), name="PreCheckout"),

    # Configure Delivery
    url(r'^menu/configure/delivery/$', views.PreCheckoutDelivery.as_view(), name="PreCheckoutDelivery"),

    # Configure Pick it Up
    url(r'^menu/configure/pickitup/$', views.PreCheckoutPickItUp.as_view(), name="PreCheckoutPickItUp"),

    # Configure Parking Lot
    url(r'^menu/configure/parkinglot/$', views.PreCheckoutParkingLot.as_view(), name="PreCheckoutParkingLot"),

    # Vistas del Menu
    url(r'^menu/$', views.MenuHome.as_view(), name="menu"),
    url(r'^menu/category/(?P<pk>[0-9]+)/$', views.CategoryProductsList.as_view(), name="ProductList"),
    url(r'^menu/category/(?P<pk_cat>[0-9]+)/product/(?P<pk_prod>[0-9]+)/$', views.MealForm.as_view(), name="MealForm"),

    # Resumen de Carro
    url(r'^menu/checkout/view-cart/$', views.ViewCartSummary.as_view(), name="ViewCartSummary"),

    url(r'^menu/checkout/payment/$',
        login_required(views.Checkout.as_view()), name="checkout"),

    url(r'^menu/checkout/thankyou/$', 
        login_required(views.ThankYouView.as_view()), name="thankyou"),
    
    url(r'^menu/view-cart/delete-item/(?P<item>[0-9]+)/$', views.DeleteItem, name="delete-item"),
    url(r'^menu/empty-cart/$', views.empty_cart, name="empty_cart"),
    url(r'^menu/closed/$', views.closed, name="closed"),
]