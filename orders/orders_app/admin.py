from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'email', 'title', 'amount', 'start_date', 'end_date', 'created_date')
    list_display_links = ('id','first_name', 'title')
    search_fields = ('first_name',)


admin.site.register(Order, OrderAdmin)