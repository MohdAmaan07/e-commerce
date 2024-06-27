from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Product,Collection,Customer,OrderItem,Order
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10','Low')
        ]
        
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)




@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    fields = ['title','slug','description','price','inventory','collection','promotion']
    actions = ['clear_inventory']
    list_display = ['title','price','inventory_status','collection_title']
    list_editable = ['price']
    search_fields = ['title']
    ordering = ['title']
    list_filter = ['collection', 'last_updated', InventoryFilter]
    list_select_related = ['collection']
    list_per_page = 10
    
    def collection_title(self,product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset : QuerySet):
        update = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update} products were successfully updated',
            messages.ERROR
        )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership', 'orders']
    list_editable = ['membership']
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']
    list_per_page = 10

    def orders(self, order):
        url = reverse('admin:core_order_changelist') + '?' + urlencode({'customer_id': str(order.id)})
        return format_html(f'<a href = "{url}">{order.order_count} Orders</a>')
        
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(order_count=Count('order'))

class OrderItem(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    min_num = 1
    max_num = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    fields = ['payment_status','customer']
    inlines = [OrderItem]
    list_display = ['id','placed_at','payment_status']
    list_editable = ['payment_status']
    ordering = ['placed_at']
    list_per_page = 10

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title','product_count']
    ordering = ['title']
    list_per_page = 10
    
    def product_count(self, collection):
        url = reverse('admin:core_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html(f'<a href = "{url}">{collection.product_count}</a>')
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(product_count=Count('product'))
    