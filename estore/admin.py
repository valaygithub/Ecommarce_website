from django.contrib import admin
from estore.models import Products


# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "pdetail", "category", "is_active"]
    list_filter = ["category", "is_active"]


admin.site.register(Products, productAdmin)
