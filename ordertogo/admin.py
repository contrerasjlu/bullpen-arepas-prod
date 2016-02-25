from django.contrib import admin
from .models import *

# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    list_display = ['code','name','description','Active']
    search_fields = ['code','name','description']

admin.site.register(category, categoryAdmin)

class productAdmin(admin.ModelAdmin):
    list_display = ['category','code','name','description', 'price','order_in_menu']
    search_fields = ['category','code','name','description','price','order_in_menu']

admin.site.register(product, productAdmin)

class PaymentBatchAdmin(admin.ModelAdmin):
	list_display = ['date', 'location','max_miles','batch_code','status']
	search_fields = ['date', 'location', 'max_miles','batch_code','status']

admin.site.register(PaymentBatch, PaymentBatchAdmin)

class GenericVariableAdmin(admin.ModelAdmin):
	list_display = ['code', 'value', 'description']
	search_fields = ['code', 'value', 'description']

admin.site.register(GenericVariable, GenericVariableAdmin)

class locationsAdmin(admin.ModelAdmin):
	list_display = ['description','location','zip_code','x_coord','y_coord']
	search_fields = ['description','location','zip_code','x_coord','y_coord']

admin.site.register(LocationsAvailable, locationsAdmin)

class OrdersAdmin(admin.ModelAdmin):
	list_display = ['order_number','order_type','user','batch','address','time']
	search_fields = ['order_number','order_type','user','batch','address','time']

admin.site.register(Order, OrdersAdmin)

class OrderDetailAdmin(admin.ModelAdmin):
	list_display = ['order_number','item','main_product','arepa_type','product_selected']
	search_fields = ['item','arepa_type']

admin.site.register(OrderDetail, OrderDetailAdmin)

class OrderPaymentAdmin(admin.ModelAdmin):
	list_display = ['order_number','cardholder_name']
	search_fields = ['order_number','cardholder_name']

admin.site.register(OrderPaymentDetail, OrderPaymentAdmin)

class RelatedImagesAdmin(admin.ModelAdmin):
	list_display = ['product','description']
	search_fields = ['description']

admin.site.register(RelatedImages, RelatedImagesAdmin)

class GuestDetailAdmin(admin.ModelAdmin):
	list_display = ['firstname','lastname','email','phone']
	search_fields = ['firstname','lastname','email','phone']

admin.site.register(GuestDetail, GuestDetailAdmin)

admin.site.register(Album)

admin.site.register(ProductRestriction)