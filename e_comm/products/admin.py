# from django.contrib import admin
# from .models import Category, Products, product_image, color, size, Variant

# class VariantInline(admin.TabularInline):
#     model = Variant
#     extra = 0

# class ProductAdmin(admin.ModelAdmin):
#     inlines = [VariantInline,]

# admin.site.register(Category)
# admin.site.register(Products, ProductAdmin)
# admin.site.register(product_image)
# admin.site.register(color)
# admin.site.register(size)
# admin.site.register(Variant)
# from django.contrib import admin
# from .models import Products, product_image, Variant


# class ProductImageInline(admin.TabularInline):
#     model = product_image
#     extra = 1


# class VariantInline(admin.TabularInline):
#     model = Variant
#     extra = 1


# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductImageInline, VariantInline]


# admin.site.register(Products, ProductAdmin)

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
