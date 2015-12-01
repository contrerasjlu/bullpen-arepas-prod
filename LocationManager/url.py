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

############ Locations Available ###############################
    # ListView para el Modelo LocationsAvailable
    url(r'^locations/list/$', 
        login_required(LocationsList.as_view(), 
            login_url='LocationManager:auth'), name='locations-list'),

    # CreateView para el Modelo LocationsAvailable
    url(r'^locations/$', 
        login_required(LocationsAvailableCreateView.as_view(), 
            login_url='LocationManager:auth'), name='locations-create'),

    # UpdateView para el Modelo Locations Available
    url(r'^locations/(?P<pk>[0-9]+)/$', 
        login_required(LocationsAvailableUpdateView.as_view(), 
            login_url='LocationManager:auth'), name='locations-update'),

################# PaymentBatches ###########################
    # ListView del Modelo PaymentBatches, tiene los abiertos y cerrados en dos dict distintos
    url(r'^batches/list$', 
        login_required(BatchesList.as_view(), 
            login_url='LocationManager:auth'), name="batches-list"),

    # CreateView del Modelo PaymentBatches
    url(r'^batches/$', 
        login_required(BatchesCreate.as_view(), 
            login_url='LocationManager:auth'), name="batches-create"),

    # UpdateView del Modelo PaymentBatches, No puede Cerrarlo
    url(r'^batches/(?P<pk>[0-9]+)/$', 
        login_required(BatchesUpdate.as_view(), 
            login_url='LocationManager:auth'), name="batches-update"),

    # Funcion para Cerrar el PaymentBatch
    url(r'^batches/close/(?P<batch>[0-9]+)/$', 
        views.CloseBatch, name="close-batch"),

    # Funcion para Cerrar el Delivery del PaymentBatch
    url(r'^batches/close/delivery/(?P<batch>[0-9]+)/$', 
        views.CloseBatchDelivery, name="close-batch-delivery"),

    # Funcion generica para el reporte de un Batch Cerrado
    url(r'^batches/(?P<pk>[0-9]+)/report/$', 
        views.BatchesReport, name="batches-report"),

######################## Orders ##############################
    
    # ListView de las ordenes por PaymentBatch por estado
    url(r'^orders/$', 
        login_required(orders.as_view(), 
            login_url='LocationManager:auth'), name="orders"),

    # ListView del Modelo Orders
    url(r'^orders/details/(?P<batch>[0-9]+)/(?P<order_status>[A-Z]+)/$', 
        login_required(HandleOrders.as_view(), 
            login_url='LocationManager:auth'), name="orders_list"),

    # ListView del Modelo OrderDetails
    url(r'^orders/details/(?P<pk>[0-9]+)/$', 
        login_required(HandleOrderDetail.as_view(), 
            login_url='LocationManager:auth'), name="orders_detail"),

    # Funcion generica de cambio de estado de una Orden
    url(r'^orders/update/(?P<pk>[0-9]+)/$', 
        views.OrderUpdate, name="order-update"),

]