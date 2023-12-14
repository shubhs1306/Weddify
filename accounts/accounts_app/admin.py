from django.contrib import admin
from .models import Vendor

# Register your models here.
class VendorAdmin (admin.ModelAdmin):
    list_display = ('id', 'service_type', 'user', 'created_date')
    list_display_links = ('id','service_type')
    search_fields = ('service_type',)

admin.site.register(Vendor, VendorAdmin)