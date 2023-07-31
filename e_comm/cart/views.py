import decimal
from decimal import Decimal
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import Cart, CartItems,wallet,GuestCart
from products.models import Variant
from coupon.models import Coupon , Usercoupon
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db.models import Sum



def add_to_cart(request, variant_id):
    variant = Variant.objects.get(id=variant_id)


    cart, created = Cart.objects.get_or_create(user=request.user)

    item = cart.cartitems_set.filter(product=variant).first()

    if item:
        if variant.stock > item.quantity :
            item.quantity += 1
            item.save()
        else:
            pass
    else:
        if variant.discount_price:
            price_item = variant.discount_price
        else:
            price_item = variant.price

        CartItems.objects.create(cart=cart,
                                product=variant, 
                                quantity=1, 
                                price=price_item)
        
    messages.success(request, "Successfullly added ptoduct to cart")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect to the cart view

# def view_cart(request):


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def view_cart(request):
   
    cart = get_object_or_404(Cart, user=request.user)
    cartitems = CartItems.objects.filter(cart = cart)
    if cartitems:

    

        # Calculate the total price before applying the coupon (subtotal)
        original_total_price = cart.get_total_price()
        if cart.cartitems_set.count() == 0:
            cart.coupons = None
        
            cart.save()

        if request.method == 'POST':
            coupon_code = request.POST.get('coupon')
            
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                usercoupon = Usercoupon.objects.filter(coupon=coupon, user=request.user) 
                
                if not coupon.is_expired and original_total_price >= coupon.mininum_amount and not usercoupon.exists():
                    # Apply coupon discount to the total price
                
                
                    cart.coupons = coupon
                    cart.save()

                    messages.success(request, 'Coupon applied successfully.')
                else:
                    messages.error(request, 'Coupon already applied')

                # Redirect to a different URL after processing the POST data
                return redirect('cart')
                    
            except ObjectDoesNotExist:
                messages.error(request, 'Coupon does not exist.')

                # Redirect to a different URL after processing the POST data
                return redirect('cart')
        if cart.coupons:
            coupon=cart.coupons
            total_price =cart.get_total_price() 
            total_price -= coupon.discount_price  
        else:
            total_price=original_total_price
    

        context = {
            'cart': cart,
            'subtotal': original_total_price,
            'total_prices': total_price,
        }

        return render(request, 'cart/shop_cart.html', context)
    else:
    
        return redirect('shop',0)


def remove_from_cart(request,item_id):
    cart_item = CartItems.objects.get(id=item_id)
    cart_item.delete()
    messages.success(request, "Successfullly removed product from cart")
    return redirect('cart')

    


def update_quantity(request):
   
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        carts = Cart.objects.get(user=request.user)
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        
        product = CartItems.objects.get(id=product_id)
        product.quantity = quantity
        if product.product.discount_price:
            product.price = product.product.discount_price * Decimal(product.quantity)
        else:
            product.price = product.product.price * Decimal(product.quantity)

        product.save()
        
        cart = product.cart
        cart.total_price = cart.get_total_price()
        cart.save()
        subtotal = cart.get_total_price()
        if carts.coupons :
            total_price = cart.total_price
            total_price -= carts.coupons.discount_price
        else:
            total_price = cart.total_price

        
        # Prepare the response data
        response_data = {
            'success': True,
            'message': 'Quantity updated successfully!',
            'price': product.price,
            'quantity': str(product.quantity),
            'total_price': total_price, 
            'subtotat':subtotal
            
        }

        return JsonResponse(response_data)
    
    response_data = {
        'success': False,
        'message': 'Invalid request',
    }
    
    return JsonResponse(response_data, status=400)

def remove_coupon(request):
    carts = Cart.objects.get(user =request.user)
    carts.coupons = None
    carts.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def view_wallet(request):
    try:
        wallets = wallet.objects.get(user=request.user)
    except ObjectDoesNotExist:
        wallet.objects.create(user=request.user)
        wallets = wallet.objects.get(user=request.user)

    context ={
        'wallets':wallets
    }

    return render(request,"cart/walllet.html",context)


# def add_to_guest_cart(request, variant_id):
#     variant = Variant.objects.get(id=variant_id)

#     # Get or create the guest session key
#     session_key = request.session.session_key
#     if not session_key:
#         request.session.save()
#         session_key = request.session.session_key

#     # Retrieve the guest session using the session key
#     try:
#         session = Session.objects.get(session_key=session_key)
#     except Session.DoesNotExist:
#         session = None

#     # Create or update the guest cart item associated with the session
#     if session:
#         cart_item, created = GuestCart.objects.get_or_create(
#             session=session,
#             product=variant,
#             defaults={'price': variant.discount_price or variant.price}  # Set the price based on variant type
#         )
#       

#         if not created:
#             cart_item.quantity += 1
#             cart_item.save()

#     return redirect('guest_cart_view')


# def guest_cart_view(request):
#     session_key = request.session.session_key
#     if not session_key:
#         request.session.save()
#         session_key = request.session.session_key

#     try:
#         session = Session.objects.get(session_key=session_key)
#     except Session.DoesNotExist:
#         session = None

#     guest_cart_items = GuestCart.objects.filter(session=session)

#     total_amount = 0

#     if guest_cart_items:
#         for guest_cart_item in guest_cart_items:
#             total_amount += guest_cart_item.get_item_price()

#     context = {
#         'guest_cart_items': guest_cart_items,
#         'total_prices': total_amount
#     }

#     return render(request, 'cart/guest_cart.html', context)

# def remove_cart_item(request,carts_id):
#     cart_item = GuestCart.objects.get(id = carts_id)
#     cart_item.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


# def update_guestcart_quantity(request):
#     if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
       
#         product_id = request.POST.get('product_id')
#         quantity = request.POST.get('quantity')
        
#         product = GuestCart.objects.get(id=product_id)
#         product.quantity = quantity
#         if product.product.discount_price:
#             product.price = product.product.discount_price * Decimal(product.quantity)
#         else:
#             product.price = product.product.price * Decimal(product.quantity)

#         product.save()
#         session_key = request.session.session_key
#         if not session_key:
#             request.session.save()
#             session_key = request.session.session_key
            
#         try:
#             session = Session.objects.get(session_key=session_key)
#         except Session.DoesNotExist:
#             session = None

#         guest_cart_items = GuestCart.objects.filter(session=session)

#         total_amount = 0

#         if guest_cart_items:
#             for guest_cart_item in guest_cart_items:
#                 total_amount += guest_cart_item.get_item_price()
        
#         # Prepare the response data
#         response_data = {
#             'success': True,
#             'message': 'Quantity updated successfully!',
#             'price': product.price,
#             'total_price':total_amount,
#             'quantity': str(product.quantity),
         
            
#         }

#         return JsonResponse(response_data)
    
#     response_data = {
#         'success': False,
#         'message': 'Invalid request',
#     }
    
#     return JsonResponse(response_data, status=400)

