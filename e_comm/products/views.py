from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.db.models import Q 
from django.db.models import Q, Min
from decimal import Decimal

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def products(request):
    cat = Category.objects.all()
    colors = color.objects.all()
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort')
    color_filter = request.GET.get('color')
    price_filter = request.GET.get('price')

    variants = Variant.objects.all()

    if category_filter and category_filter != 'all':
        variants = variants.filter(product__category__name=category_filter)

    if search_query:
        variants = variants.filter(
            Q(product__name__icontains=search_query) | Q(product__descriptions__icontains=search_query)
        )

    if price_filter:
        if price_filter == '0-500':
            variants = variants.filter(price__range=(Decimal('0.00'), Decimal('500.00')))
        elif price_filter == '500-2000':
            variants = variants.filter(price__range=(Decimal('500.00'), Decimal('2000.00')))
        elif price_filter == '2000-4000':
            variants = variants.filter(price__range=(Decimal('2000.00'), Decimal('4000.00')))
        elif price_filter == '4000-6000':
            variants = variants.filter(price__range=(Decimal('4000.00'), Decimal('6000.00')))
        else:
            variants = variants.filter(price__gte=Decimal('6000.00'))

    if color_filter and color_filter != 'all':
        variants = variants.filter(color__color=color_filter)

    if sort_by == 'popularity':
        variants = variants.order_by('-product__created_at')
    elif sort_by == 'newness':
        variants = variants.order_by('-product__created_at')
    elif sort_by == 'price_low_to_high':
        variants = variants.order_by('price')
    elif sort_by == 'price_high_to_low':
        variants = variants.order_by('-price')

    # Number of products to display per page
    products_per_page = 8

    # Create a Paginator object
    paginator = Paginator(variants, products_per_page)

    # Get the requested page number from the query parameters
    page_number = request.GET.get('page')

    try:
        # Get the products for the requested page
        variants = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        variants = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results.
        variants = paginator.page(paginator.num_pages)

    context = {
        'colors': colors,
        'variant': variants,
        'cat': cat,
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

