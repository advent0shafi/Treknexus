import decimal
from decimal import Decimal
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import Cart, CartItems,wallet
from products.models import Variant
from coupon.models import Coupon , Usercoupon
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404



def add_to_cart(request, variant_id):
    variant = Variant.objects.get(id=variant_id)

    # Check if a cart exists for the user, or create a new one
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    item = cart.cartitems_set.filter(product=variant).first()

    if item:
        # If the item already exists, increment the quantity
        item.quantity += 1
        item.save()
    else:
        # If the item doesn't exist, create a new cart item
        CartItems.objects.create(cart=cart, product=variant, quantity=1, price=variant.price)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect to the cart view

# def view_cart(request):


def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = cart.get_total_price()

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            usercoupon = Usercoupon.objects.filter(coupon = coupon ,user = request.user) 
            
            if not coupon.is_expired and total_price >= coupon.mininum_amount and not usercoupon.exists():
                # Apply coupon discount to the total price
                total_price -= coupon.discount_price

                # Set the applied coupon in the cart
                Usercoupon.objects.create(
                    user = request.user,
                    coupon = coupon, used = True, 
                    total_price = total_price
                    )
                cart.coupons = coupon
                cart.save()

                messages.success(request, 'Coupon applied successfully.')
            else:
                messages.error(request, 'Invalid coupon.')
                
        except ObjectDoesNotExist:
            messages.error(request, 'Coupon does not exist.')

    # Check if the cart is empty and set the coupon to None
    if cart.cartitems_set.count() == 0:
        cart.coupons = None
        cart.save()
    context = {
        'cart': cart,
        'total_price': total_price,
    }

    return render(request, 'cart/shop_cart.html', context)


def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        print(item_id)
        cart_item = CartItems.objects.get(id=item_id)
        cart_item.delete()

        return redirect('cart')

    return render(request, 'cart/shop_cart.html')


def update_quantity(request):
   
  
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        
        product = CartItems.objects.get(id=product_id)
        product.quantity = quantity
        product.price = product.product.price * Decimal(product.quantity)
        product.save()
        
        # Prepare the response data
        response_data = {
            'success': True,
            'message': 'Quantity updated successfully!',
            'price': str(product.price),
            'quantity': str(product.quantity),
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

def view_wallet(request):
    try:
        wallets = wallet.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Handle the case when the wallet doesn't exist for the user
        # For example, you can create a new wallet for the user
        wallet.objects.create(user=request.user)
        wallets = wallet.objects.get(user=request.user)

    context ={
        'wallets':wallets
    }

    return render(request,"cart/walllet.html",context)