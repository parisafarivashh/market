from django.contrib import admin

from product.models import Category, SubCategory, Product, Color, Detail


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_id', 'category_name']
    list_filter = ['name']
    search_fields = ['name']

    def category_name(self, obj):
        return obj.category_id.name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'rank', 'seller_id', 'seller_name', 'sub_category']
    list_filter = ['name', 'rank']
    search_fields = ['name', 'seller_id__username__startswith']
    readonly_fields = ['seller_id', 'rank']

    def seller_name(self, obj):
        return obj.seller_id.username


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    list_filter = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['color_id', 'size', 'count', 'product_id']
    list_filter = ['price', 'size']
    search_fields = ['color_id__name', 'product_id__name']

