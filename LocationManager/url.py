from django.conf.urls import url
from LocationManager import views
from LocationManager.views import LocationsList, BatchesList, HandleOrders, HandleOrderDetail, orders, BatchesCreate, BatchesUpdate, LocationsAvailableCreateView, LocationsAvailableUpdateView
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    # Vistas autogeneradas
    url(r'^login/$', views.auth, name='auth'),
    url(r'^logout/$', views.logout_user, name='logout'),

    # Vistas del Location Manager
    url(r'^home/$', views.index, name="index"),

    # Vista Generica de Consulta de los Locations Availables
    url(r'^locations/list/$', 
        login_required(LocationsList.as_view(), login_url='/location/login'), 
        name='locations-list'),

    url(r'^locations/$', 
        login_required(LocationsAvailableCreateView.as_view(), login_url='/location/login'), 
        name='locations-create'),

    url(r'^locations/(?P<pk>[0-9]+)/$', 
        login_required(LocationsAvailableUpdateView.as_view(), login_url='/location/login'), 
        name='locations-update'),

    # Vista Generica de Consulta de los Lotes abiertos y Cerrados
    url(r'^batches/list$', 
        login_required(BatchesList.as_view(), login_url='/location/login'), 
        name="batches-list"),

    url(r'^batches/$', 
        login_required(BatchesCreate.as_view(), login_url='/location/login'), 
        name="batches-create"),

    url(r'^batches/(?P<pk>[0-9]+)/$', 
        login_required(BatchesUpdate.as_view(), login_url='/location/login'), 
        name="batches-update"),

    url(r'^batches/close/(?P<batch>[0-9]+)/$', views.CloseBatch, name="close-batch"),

    url(r'^batches/close/delivery/(?P<batch>[0-9]+)/$', views.CloseBatchDelivery, name="close-batch-delivery"),


    # Vista de los Estados de las Ordenes
    url(r'^orders/$', 
        login_required(orders.as_view(), login_url='/location/login'), 
        name="orders"),

    # Vista Generica de vista del listado de ordenes
    url(r'^orders/details/(?P<batch>[0-9]+)/(?P<order_status>[A-Z]+)/$', 
        login_required(HandleOrders.as_view(), login_url='/location/login/'), 
        name="orders_list"),

    # Vista Generica de vista del Detalle de una orden
    url(r'^orders/details/(?P<id_order>[0-9]+)/$', 
        login_required(HandleOrderDetail.as_view(), login_url='/location/login/'), 
        name="orders_detail"),

]