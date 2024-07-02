from django.contrib import admin

from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date_ordered', 'complete']
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)