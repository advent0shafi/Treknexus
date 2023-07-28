from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.db.models import Q 
from django.db.models import Q, Min
from decimal import Decimal


from django.http import JsonResponse


# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    
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




def shop(request, category_id):
   
    if category_id == 0:
      
        variants =Variant.objects.all()
    else:
        category = get_object_or_404(Category, id=category_id)
        variants = Variant.objects.filter(product__category=category)
    colors = color.objects.all()
    catogeris = Category.objects.all()
    search_query = request.GET.get('search')
    price_filter = request.GET.get('price')
    color_filter = request.GET.get('color')
    sort_by = request.GET.get('sort')

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
    items_per_page = 16

    page_number = request.GET.get('page')

    paginator = Paginator(variants, items_per_page)
    try:
        variants = paginator.page(page_number)
    except PageNotAnInteger:
        variants = paginator.page(1)
    except EmptyPage:
        variants = paginator.page(paginator.num_pages)


    context ={
        'colors': colors,
        'variants': variants,
        'cats': catogeris,
    }

    return render(request, "products/catogery.html", context)

def filter(request, category_id):
    if category_id == 0:
        variants = Variant.objects.all()
    else:
        category = get_object_or_404(Category, id=category_id)
        variants = Variant.objects.filter(product__category=category)

    colors = color.objects.all()
    sizes = size.objects.all()
    catogeris = Category.objects.all()

    # Get selected color filters
    selected_colors = request.GET.getlist('color')

    # Get selected size filters
    selected_sizes = request.GET.getlist('size')

    # Get selected price filter
    selected_price = request.GET.get('price')

    # Get selected sort option
    selected_sort = request.GET.get('sort')

    # Apply the filters
    if 'all' not in selected_colors:
        variants = variants.filter(color__color__in=selected_colors)

    if 'all' not in selected_sizes:
        variants = variants.filter(size__size__in=selected_sizes)

    if selected_price:
        if selected_price == '0-50':
            variants = variants.filter(price__range=(Decimal('0.00'), Decimal('50.00')))
        elif selected_price == '50-100':
            variants = variants.filter(price__range=(Decimal('50.00'), Decimal('100.00')))
        elif selected_price == '100-150':
            variants = variants.filter(price__range=(Decimal('100.00'), Decimal('150.00')))
        elif selected_price == '150-200':
            variants = variants.filter(price__range=(Decimal('150.00'), Decimal('200.00')))
        else:
            variants = variants.filter(price__gte=Decimal('200.00'))

    if selected_sort == 'popularity':
        variants = variants.order_by('-product__created_at')
    elif selected_sort == 'newness':
        variants = variants.order_by('-product__created_at')
    elif selected_sort == 'price_low_to_high':
        variants = variants.order_by('price')
    elif selected_sort == 'price_high_to_low':
        variants = variants.order_by('-price')

    # Number of products to display per page
    items_per_page = 16
    page_number = request.GET.get('page')
    paginator = Paginator(variants, items_per_page)

    try:
        variants = paginator.page(page_number)
    except PageNotAnInteger:
        variants = paginator.page(1)
    except EmptyPage:
        variants = paginator.page(paginator.num_pages)

    context = {
        'colors': colors,
        'sizes': sizes,
        'variants': variants,
        'cats': catogeris,
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
        'selected_price': selected_price,
        'selected_sort': selected_sort,
    }

  
    return render(request, "products/filter_test.html", context)