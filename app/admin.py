from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'locality', 'city', 'zipcode', 'state')
    search_fields = ('user__username', 'name', 'city', 'state')
    list_filter = ('state', 'city')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'selling_price', 'discount_price', 'brand', 'category')
    search_fields = ('title', 'brand', 'category')
    list_filter = ('category', 'brand')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'totalCost')
    search_fields = ('user__username', 'product__title')
    list_filter = ('user',)

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'totalCost')
    search_fields = ('user__username', 'customer__name', 'product__title', 'status')
    list_filter = ('status', 'ordered_date')

    def totalCost(self, obj):
        return obj.totalCost
    totalCost.short_description = 'Total Cost'
