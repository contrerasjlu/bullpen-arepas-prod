from django.conf.urls import url
from ordertogo import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^categories/$', views.Category.as_view()),
    #url(r'^products/$', views.Product.as_view()),
    url(r'^categories/(?P<CatId>[0-9]+)/products/$', views.Product_By_Category),
    url(r'^categories/(?P<CatId>[0-9]+)/products/(?P<ProdId>[0-9]+)/$', views.Product_Detail),

    url(r'^texts/$', views.Texts.as_view()),
    url(r'^texts/(?P<code>[\w]+)/$', views.TextDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)