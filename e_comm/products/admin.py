from django.contrib import admin
from .models import Category, Products, color, size, Variant, product_image
from django.forms import inlineformset_factory
class VariantInline(admin.TabularInline):
    model = Variant
    

class ProductImageInline(admin.TabularInline):
    model = product_image
    extra = 1

class VariantAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


class ProductsAdmin(admin.ModelAdmin):
    inlines = [VariantInline]


class VariantAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
# VariantInlineFormSet = inlineformset_factory(
#     Products,
#     Variant,
#     fields=('title', 'size', 'color', 'variant_image', 'quantity', 'price', 'stock'),
#     extra=1,
# # )
# class ProductsAdmin(admin.ModelAdmin):
#     inlines = [VariantInlineFormSet]

admin.site.register(Category)
admin.site.register(Products, ProductsAdmin)
admin.site.register(color)
admin.site.register(size)
admin.site.register(Variant)
admin.site.register(product_image)
