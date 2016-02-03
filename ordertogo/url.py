from django.conf.urls import url
from ordertogo import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^onthegame/categories/$', views.api_WebCategories.as_view()),
    url(r'^onthegame/categories/(?P<CatId>[0-9]+)/$', views.api_WebCategoryDetails.as_view()),
    url(r'^onthegame/categories/(?P<CatId>[0-9]+)/products/$', views.api_WebProducts.as_view()),
    url(r'^onthegame/categories/(?P<CatId>[0-9]+)/products/(?P<ProdId>[0-9]+)/$', views.api_WebProductsDetails.as_view()),

    url(r'^texts/$', views.Texts.as_view()),
    url(r'^texts/(?P<code>[\w]+)/$', views.TextDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)