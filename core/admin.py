from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from core.models import Category, Product, Variant


class VariantInline(StackedInline):
    model = Variant


class ProductAdmin(ModelAdmin):
    list_display = ['id', 'title', 'creator__title', 'category__title']
    list_filter = ['id', 'title', 'creator__title', 'category__title']
    readonly_fields = ['id', 'creator', 'category']
    list_select_related = ['creator', 'category']
    ordering = ['id']
    inlines = [VariantInline]


class CategoryAdmin(ModelAdmin):
    list_display = ['id', 'title']
    list_filter = ['id', 'title']
    readonly_fields = ['id']
    ordering = ['id']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
