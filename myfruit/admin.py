from django.contrib import admin
from .models import MaincategoryModel,ProductModel,cartmodel,wishlistmodel,CustomeraddressModel,contactmodel
# Register your models here.


@admin.register(MaincategoryModel)
class MaincategoryModelAdmin(admin.ModelAdmin):
    list_display = ("image", "name")[::-1]


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ( "description", "sell_price", "discount_price", "discount", "og_price", "image", "name", "mcate")


@admin.register(cartmodel)
class cartmodelAdmin(admin.ModelAdmin):
    list_display = ( "quantity", "product", "user")[::-1]


@admin.register(wishlistmodel)
class wishlistmodelAdmin(admin.ModelAdmin):
    list_display = ("product", "user")[::-1]


@admin.register(CustomeraddressModel)
class CustomeraddressModelAdmin(admin.ModelAdmin):
    list_display = ("add2", "add1", "pincode", "city", "state", "counrty", "mobile", "email", "lname", "fname", "user")[::-1]


@admin.register(contactmodel)
class contactmodelAdmin(admin.ModelAdmin):
    list_display = ("message", "subject", "email", "name", "user")[::-1]
