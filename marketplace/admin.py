from django.contrib import admin

from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created', 'modified')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created', 'modified')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
