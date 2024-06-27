from django.shortcuts import render
from .models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def home(request):
    tag = TaggedItem.objects.get_tag_for(Product, 1)
    return render(request, 'core/index.html', {'tags': tag})
