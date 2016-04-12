from django.contrib import admin
from .models import *

# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    list_display = ['code','name','description','show_in_menu','order','Active']
    search_fields = ['code','name','description']
    list_filter = ['Active', 'show_in_menu']

admin.site.register(category, categoryAdmin)

class productAdmin(admin.ModelAdmin):
    list_display = ['name', 'category','code','description', 'price','order_in_menu','Active']
    search_fields = ['category__name','code','name','description','price','order_in_menu']
    list_filter = ['category__name', 'Active', 'price']
    fieldsets = [
        (None,          {'fields': ['category','code','name','description','allow_type','Active']}),
        ('Meats',       {'fields': ['allow_extras','extras'], 'classes': ['collapse']}),
        ('Additionals', {'fields': ['allow_additionals','max_additionals'], 'classes': ['collapse']}),
        ('Vegetables',  {'fields': ['allow_vegetables','max_vegetables'], 'classes': ['collapse']}),
        ('Extras',      {'fields': ['allow_paid_extras','max_paid_extras'], 'classes': ['collapse']}),
        ('Sauces',      {'fields': ['allow_sauces','max_sauces'], 'classes': ['collapse']}),
        ('Drinks',      {'fields': ['allow_drinks'], 'classes': ['collapse']}),
        ('Quantity',    {'fields': ['allow_qtty','max_qtty']}),
        ('Price & Menu',{'fields': ['price','order_in_menu','image']}),
    ]
    actions = ['InactivateSelection','ActivateSelection']

    def InactivateSelection(self, request, queryset):

    	if queryset.count() == 0:
    		self.message_user(request, "You must select at least one product to inactivate",level=40)

    	for Product in queryset:
    		Product.Active = False
    		Product.save()

    	self.message_user(request, '%d items were Inactivated' % (queryset.count()))

    InactivateSelection.short_description = "Inactivate Selected Products"

    def ActivateSelection(self, request, queryset):
    	if queryset.count() == 0:
    		self.message_user(request, "You must select at least one product to activate",level=40)

    	for Product in queryset:
    		Product.Active = True
    		Product.save()

    	self.message_user(request, '%d item were Activated' % (queryset.count()))

    ActivateSelection.short_description = "Activate Selected Products"


admin.site.register(product, productAdmin)

class PaymentBatchAdmin(admin.ModelAdmin):
	list_display = ['date', 'location','max_miles','batch_code','status']
	search_fields = ['date', 'location__description', 'max_miles','batch_code','status']
	list_filter = ['date', 'status', 'location__description']

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
	list_filter = ['order_type']

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