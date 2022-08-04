from django.contrib import admin

from order.models import Order, ItemOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_name', 'paid']
    list_filter = ['user']
    search_fields = ['user__username', ]
    readonly_fields = ['user', 'paid']

    def user_name(self, obj):
        return obj.user.username


@admin.register(ItemOrder)
class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'order_user_name', 'order_user_id']
    list_filter = ['order', 'count']
    search_fields = ['order__user__username__startswith', ]
    readonly_fields = ['price', 'detail', 'order']

    def order_user_name(self, obj):
        return obj.order.user.username

    def order_user_id(self, obj):
        return obj.order.user.id

