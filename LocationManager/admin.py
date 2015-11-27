from django.contrib import admin
from .models import *

# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display = ['label','url','imgClass','activeOn', 'order', 'child_of']
    search_fields = ['label','url','imgClass','activeOn', 'order']

admin.site.register(location_admin_menu, MenuAdmin)
