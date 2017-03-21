from django.contrib import admin

# Register your models here.
from .models import Product

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "slug", "created_at", "modified_at", "description"]

    search_fields = ["name", "description"]

    class Meta:
        model = Product

# Registers the post model into our admin site.
admin.site.register(Product, ProductModelAdmin)