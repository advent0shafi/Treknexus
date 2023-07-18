from django.shortcuts import render,redirect,get_object_or_404
from products.models import *
from django.contrib.auth.models import User
from .forms import *
from django.db.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from userorder.models import *
from products.models import Category, Products, Variant, color, size, product_image
from django.contrib.auth import authenticate,login,logout
from datetime import date
from datetime import datetime
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from django.contrib.auth.forms import AuthenticationForm
from coupon.models import Coupon


# Create your views here.


def admin_home(request):
    if request.user.is_superuser:
       
        # Get the total order count and total price for all orders
        order_count = Order.objects.exclude(payment_status='CANCELLED').count()
        total_price = Order.objects.exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']
        categories = Category.objects.all()
        data = []

        for category in categories:
            product_count = Products.objects.filter(category=category).count()
            data.append(product_count)

        today = timezone.now().date()
        today_orders = Order.objects.filter(order_date__date=today)
        order_count_today = today_orders.count()
        total_price_today = sum(order.total_price for order in today_orders)
        
        recent_orders = Order.objects.order_by('-order_date')[:5]
        
        start_date = request.GET.get('start_date')
        
        end_date = request.GET.get('end_date')
        pending_order_count = Order.objects.filter(payment_status='PENDING').count()

        # Get the count of delivered orders
        delivered_order_count = Order.objects.filter(payment_status='PAID').count()
        
        
        context = {
                'pending_order_count': pending_order_count,
                'delivered_order_count': delivered_order_count,
                'categories': categories,
                 'data': data,
                'start_date': start_date,
                'end_date': end_date,
                'recent_orders':recent_orders,
                'order_count': order_count,
                'total_price': total_price,
                'order_count_today': order_count_today,
                'total_price_today': total_price_today,
            }
        # Filter orders based on the provided date range
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Query the Order model and annotate the total price per date within the specified date range
            daily_totals = Order.objects.exclude(payment_status='CANCELLED').filter(
                order_date__date__range=[start_date, end_date]
            ).annotate(date=TruncDate('order_date')).values('date').annotate(total=Sum('total_price')).order_by('date')

            top_product = Variant.objects.filter(orderitem__order__order_date__date__range=[start_date, end_date]).annotate(
                sale_count=Count('orderitem')
            ).order_by('-sale_count')[:3]
            orders_within_period = Order.objects.filter(
            order_date__date__range=[start_date, end_date]
        )

        # Get the count of pending orders within the date range
            pending_order_count = orders_within_period.filter(payment_status='PENDING').count()

        # Get the count of delivered orders within the date range
            delivered_order_count = orders_within_period.filter(payment_status='PAID').count() 
            # Pass the start and end dates to the template
            context = {
                'pending_order_count': pending_order_count,
                'delivered_order_count': delivered_order_count,
                'top_product':top_product,
                'categories': categories,
                'data': data,
                'start_date': start_date,
                'end_date': end_date,
                'daily_totals': daily_totals,
                'recent_orders':recent_orders,
                'order_count': order_count,
                'total_price': total_price,
                'order_count_today': order_count_today,
                'total_price_today': total_price_today,
            }
            return render(request, 'admin/admin_home.html', context)
    

        return render(request, 'admin/admin_home.html',context)
    
    return redirect('admin_signin')


def admin_signin(request):
   
   if request.method == 'POST':
      username = request.POST["username"]
     
      pass1 = request.POST['pass1']
    
      user = authenticate(username = username, password = pass1)

      if user is not None and user.is_superuser :
        
          login(request,user)
          return redirect('admin_home')
      else:
          return redirect('admin_signin')
      
   return render(request,'admin/signin.html')

def adminpage(request):
    if request.user.is_superuser :
        products = Products.objects.all()
        return render(request,'admin/dashboard.html',{"products":products})
    else:
        return redirect('admin_signin')
  
def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    # Soft delete logic
    product. is_avaiable = False
    product.save()

    return redirect('adminpage') 

def activate_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    # Soft delete logic
    product. is_avaiable = True
    product.save()

    return redirect('adminpage') 

def userlist(request):

    userlist = User.objects.all()

    return render(request,'admin/userlist.html',{'userlist':userlist})


def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('userlist'))  # Redirect to user list page after blocking

def unblock_user(request, user_id):
    pro = get_object_or_404(Products, id=user_id)
    pro.is_active = True
    pro.save()
    return HttpResponseRedirect(reverse('userlist'))  # Redirect to user list page after unblocking



def addproduct(request):
    if request.method == 'POST':
        # Retrieve form data from the request
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        variant_titles = request.POST.get('variant_title')
        sizes = request.POST.get('sizes')
        colors = request.POST.get('colors')
        display_image = request.FILES.get('display_image')
        images = request.FILES.getlist('images')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        stock = request.POST.get('stock')
        variant_titles = request.POST.get('variant_title')

        # Create the product
        category = Category.objects.get(id=category_id)
        product = Products.objects.create(
            name=product_name,
            descriptions=description,
            category=category
            )
        color_slt = color.objects.get(color=colors)
        size_slt =size.objects.get(size=sizes)
        # Create variants for the product
        variant = Variant.objects.create(
            title = variant_titles,
            product=product,
            color=color_slt,
            size=size_slt,
            quantity =quantity,
            price=price,
            stock=stock,
            variant_image=display_image
        )

        # Create product images
        for image in images:
            product_image.objects.create(product=variant, image=image)

        return redirect('adminpage')  # Redirect to the product list page after successful submission

    # Retrieve categories, colors, and sizes for the form
    categories = Category.objects.all()
    colors = color.objects.all()
    sizes = size.objects.all()

    context = {
        'categories': categories,
        'colors': colors,
        'sizes': sizes
    }

    return render(request, 'admin/productadd.html', context)

            
def product_view(request,product_id):
    product = Variant.objects.filter(product=product_id)
    pro = Products.objects.get(id=product_id)
    context ={

        'product':product,
        'pro':pro
    }
    return render(request,'admin/product_view.html',context)


def variant_add(request,product_id):
    if request.method == 'POST':
        # Retrieve form data from the request
        variant_titles = request.POST.get('variant_title')
    
        colors = request.POST.get('colors')
        sizes = request.POST.get('sizes')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        display_image = request.FILES.get('display_image')
        images = request.FILES.getlist('images')

        # Create the variant
        product = Products.objects.get(id=product_id)
        color_slt = color.objects.get(color=colors)
        size_slt =size.objects.get(size=sizes)
        variant = Variant.objects.create(
            title=variant_titles,
            product=product,
            color=color_slt,
            size=size_slt,
            quantity=quantity,
            price=price,
            stock=stock,
            variant_image=display_image
        )

        # Create product images
        for image in images:
            product_image.objects.create(product=variant, image=image)

        return redirect('product_view',product_id=product_id)  # Redirect to the admin page after successful submission

    # Retrieve products, colors, and sizes for the form
    products = Products.objects.all()
    colors = color.objects.all()
    sizes = size.objects.all()

    context = {
        'products': products,
        'colors': colors,
        'sizes': sizes
    }

    return render(request, 'admin/variant_add.html', context)




def variant_edit(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)

    if request.method == 'POST':
        # Retrieve form data from the request
        variant_titles = request.POST.get('variant_title')
        colors = request.POST.get('colors')
        sizess = request.POST.get('sizes')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        display_image = request.FILES.get('display_image')
        images = request.FILES.getlist('images')
        colorss =color.objects.get(id = colors)
        sizes =size.objects.get(size = sizess)

        # Update the variant
        variant.title = variant_titles
        variant.color = colorss
        variant.size = sizes
        variant.quantity = quantity
        variant.price = price
        variant.stock = stock

        if display_image:
            variant.variant_image = display_image

        variant.save()

        # Update or create product images
        for image in images:
            product_image.objects.create(product=variant, image=image)

        return redirect('product_view', product_id=variant.product.id)  # Redirect to the product view page after successful update
    colors = color.objects.all()
    sizes = size.objects.all()

    context = {
        'variant': variant,
        'colors': colors,
        'sizes': sizes
    }

    return render(request, 'admin/variant_edit.html', context)




def catogery(request):
    cat =Category.objects.all()
    context = {
        'cat':cat
    }
    return render(request,'admin/catogery.html',context)

def catogery_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if name and image:
            catogery = Category(name=name, image=image)
            catogery.slug = slugify(catogery.name)
            catogery.save()
            return redirect('catogery')


        
    return render(request, 'admin/catogery_add.html')


def order_all(request):
    order = Order.objects.all()
    context ={
        'order':order
    }
    return render(request,'admin/all_orders.html',context)

def order_views(request,order_id):
    orders = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=orders)
    total_price = sum(item.price * item.quantity for item in items)

    context = {
        'orders':orders,
        'items':items,
        'total_price':total_price
    }
   

    return render(request,'admin/order_views.html',context)


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.payment_status != 'PAID' and order.payment_status != 'CANCELLED':
        # Update the payment status to 'CANCELLED'
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
        
            print(item.quantity)
            variant = item.product  
            variant.stock += item.quantity
            variant.save()
          

        order.payment_status = 'CANCELLED'
        order.save()

    return redirect('order_all')



def catogery_delete(request,catogery_id):
    catogerys = get_object_or_404(Category,id = catogery_id)
    catogerys.delete()
     
    return redirect('catogery')  

# def download_order_pdf(request, order_id):
#     # Fetch the order details from the database
#     order = Order.objects.get(id=order_id)

#     # Generate the PDF content
#     template_path = 'admin/downloadpdf.html'  # Create a new template for the PDF content
#     context = {'order': order}
#     template = get_template(template_path)
#     html = template.render(context)
#     result = BytesIO()
    
#     # Create the PDF document
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

#     if not pdf.err:
#         # Set the response headers for downloading the PDF
#         response = HttpResponse(result.getvalue(), content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'
#         return response

#     return HttpResponse('Error generating PDF', status=500)

# def download_order_pdf2(request,order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'admin/downloadpdf.html', {'order': order})


def coupon_view(request):
    coupon = Coupon.objects.all()
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        discount_price = request.POST.get('discount_amount')
        minimum_amount = request.POST.get('minimum_amount')
        is_expired = 'is_expired' in request.POST

        # Create a new Coupon object
        coupon = Coupon.objects.create(
            coupon_code=coupon_code,
            discount_price=discount_price,
            mininum_amount=minimum_amount,
            is_expired=is_expired
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context ={
        'coupon':coupon
    }

    return render(request,"admin/coupon.html",context)


def coupon_expired(request,coupon_id):

    coupon = Coupon.objects.get(id = coupon_id)
    coupon.is_expired = True
    coupon.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))\
    


def coupon_activate(request,coupon_id):

    coupon = Coupon.objects.get(id = coupon_id)
    coupon.is_expired = False
    coupon.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

