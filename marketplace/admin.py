from django.contrib import admin

from .models import Category, Product, Sale

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created', 'modified')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created', 'modified')

class SaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'announcement_date', 'start_date', 'end_date')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)
