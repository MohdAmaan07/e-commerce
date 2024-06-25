from django.shortcuts import render
from .models import Product
# Create your views here.
def home(request):
    product = Product.objects.all()
    for p in product:
        print(p)
    return render(request, 'core/index.html')
