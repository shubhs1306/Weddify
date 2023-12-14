from django.contrib import admin
from .models import Service

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'service_type', 'featured_package_price', 'created_date', 'vendor_id' ,'is_featured')
    list_display_links = ('id','title', 'service_type')
    search_fields = ('title', 'service_type')
    list_editable = ('is_featured',)

admin.site.register(Service, ServiceAdmin)