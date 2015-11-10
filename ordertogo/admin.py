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
	list_display = ['date','location','x_coord','y_coord','max_miles','batch_code','status']
	search_fields = ['date','location','x_coord','y_coord','max_miles','batch_code','status']

admin.site.register(PaymentBatch, PaymentBatchAdmin)