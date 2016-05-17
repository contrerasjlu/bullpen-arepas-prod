from django.contrib import admin
from .models import *

class categoryAdmin(admin.ModelAdmin):
    list_display = ['category','override_desc','show_price','webImage']
    search_fields = ['category','override_desc','show_price','webImage']

admin.site.register(WebCategory, categoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    '''
        Admin View for Product
    '''
    list_display = ('webCat','product','webImage',)
    search_fields = ['webCat','product','webImage']

admin.site.register(WebProduct, ProductAdmin)

class WebTextAdmin(admin.ModelAdmin):
    '''
        Admin View for WebText
    '''
    list_display = ('code','name','text','active')
    search_fields = ['code','name','text','active']

admin.site.register(WebText, WebTextAdmin)

class WebInfoAdmin(admin.ModelAdmin):
    '''
        Admin View for WebInfo
    '''
    list_display = ('name','email','info')

admin.site.register(WebInfo, WebInfoAdmin)

class WebCarrouselAdmin(admin.ModelAdmin):
    '''
        Admin View for WebCarrousel
    '''
    list_display = ('alt','order','active')

admin.site.register(WebCarrousel, WebCarrouselAdmin)

class WebGalleryAdmin(admin.ModelAdmin):
    '''
        Admin View for WebGallery
    '''
    list_display = ('Event','Alternative','Caption','Order','State')

admin.site.register(WebGallery, WebGalleryAdmin)