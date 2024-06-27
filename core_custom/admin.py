from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from core.admin import ProductAdmin
from core.models import Product
from tags.models import TaggedItem
# Register your models here.

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    
    
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]
    
admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)