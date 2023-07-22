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
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db.models import Sum



def add_to_cart(request, variant_id):
    variant = Variant.objects.get(id=variant_id)


    cart, created = Cart.objects.get_or_create(user=request.user)

    item = cart.cartitems_set.filter(product=variant).first()

    if item:
        
        item.quantity += 1
        item.save()
    else:
        if variant.discount_price:
            print('>>>>>>>>>>>>>>>>>>',variant.discount_price)
            price_item = variant.discount_price
        else:
            price_item = variant.price

        CartItems.objects.create(cart=cart,
                                product=variant, 
                                quantity=1, 
                                price=price_item)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect to the cart view

# def view_cart(request):


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = CartItems.objects.filter(cart=cart)
    total_prices = items.aggregate(total_price=Sum('price'))['total_price'] or 0
   
    # total_price = cart.get_total_price()

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            usercoupon = Usercoupon.objects.filter(coupon=coupon, user=request.user) 
            
            if not coupon.is_expired and total_price >= coupon.mininum_amount and not usercoupon.exists():
                # Apply coupon discount to the total price
                total_price -= coupon.discount_price

          
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

   
    if cart.cartitems_set.count() == 0:
        cart.coupons = None
        cart.save()
    context = {
        'cart': cart,
    
        'total_prices': total_prices,
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
        if product.product.discount_price:
            product.price = product.product.discount_price * Decimal(product.quantity)
        else:
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