from django.conf.urls import url
from website import views

urlpatterns = [
    url(r'^home/$', views.index, name="index"),
    url(r'^menu/$', views.menu, name="menu"),
]