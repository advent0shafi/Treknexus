from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.db.models import Q

# Create your views here.


def products(request):
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')

    if category_filter and category_filter != 'all':
        products = Products.objects.filter(category__name=category_filter)
    else:
        products = Products.objects.all()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(descriptions__icontains=search_query)
        )

    context = {
        'products': products,
        'cat': categories,
        'search_query': search_query,
    }

    return render(request, 'products/shop.html', context)

def product_details(request,slug):
  
    
    pro = Variant.objects.get(slug=slug)
    cat = pro.product.category 
    
    
    product = Products.objects.filter( category=cat).exclude(variant__slug=slug)
    

    pros = Variant.objects.get(slug=slug)

    context = {
        'pros':pros,
        'product':product
               }
    return render(request,'products/products_details.html',context)

