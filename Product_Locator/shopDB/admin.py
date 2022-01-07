from django.contrib import admin
from .models import User,Product,Discount,Shop, Log

# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('ShopID', 'ShopName', 'UserName', 'Location')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('ProductID', 'ProductName', 'BuyingPrice', 'SellingPrice' , 'Quantity', 'image')



class DiscountAdmin(admin.ModelAdmin):
    list_display = ('DiscountID', 'Percentage', 'DiscountAmount')



class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'Mobile', 'status')



class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'Buyer_Name', 'Buyer_Mobile_No', 'product', 'shop', 'Net_Price', 'No_of_prods')



admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(User)
admin.site.register(Log)