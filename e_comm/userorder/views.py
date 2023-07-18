from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from userprofile.models import *
from cart.models import *
from userorder.models import*
import razorpay
from django.conf import settings
from django.http import JsonResponse
from coupon.models import Coupon

# Create your views here.

def checkout(request, address_id):
    user_add = get_object_or_404(UserAddress, id=address_id, user=request.user)
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None
    
    items = CartItems.objects.filter(cart=cart)
    subtotal = items.aggregate(total_price=Sum('price'))['total_price'] or 0
    
    total_price = subtotal
    if cart and cart.coupons:
        coupon = get_object_or_404(Coupon, coupon_code=cart.coupons)
        min_amount = coupon.discount_price
        total_price = subtotal - min_amount
    else:
        total_price = subtotal

    context = {
        'cart':cart,
        'subtotal': subtotal,
        'user_add': user_add,
        'cart': cart,
        'total_price': total_price
    }

    return render(request, "order/checkout.html", context)


def online_payment_order(request, userId):
    if request.method == 'POST':
        payment_id = request.POST.getlist('payment_id')[0]
        orderId = request.POST.getlist('orderId')[0]
        signature = request.POST.getlist('signature')[0]
        user_adds = UserAddress.objects.get(id=userId, user=request.user)
        cartss = Cart.objects.get(user=request.user)
        items = CartItems.objects.filter(cart=cartss)
       
        subtotal = items.aggregate(total_price=Sum('price'))['total_price'] or 0
    
        total_price = subtotal
        if cartss and cartss.coupons:
            coupon = get_object_or_404(Coupon, coupon_code=cartss.coupons)
            min_amount = coupon.discount_price
            total_price = subtotal - min_amount
        else:
            total_price = subtotal
    
        order = Order.objects.create(
            user=request.user,
            address=user_adds,
            total_price=total_price,
            payment_status='PAID',
            payment_method='PAYPAL',
            razor_pay_payment_id=payment_id,
            razor_pay_payment_signature=signature,
            razor_pay_order_id = orderId,
        )
       
        coupon = get_object_or_404(Cart, user=request.user)
        coupon.coupons = None
        coupon.save()

        for cart_item in items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity
                # Set other fields as necessary
            )
        variant = cart_item.product
        variant.stock -= cart_item.quantity
        variant.save()
        orderId = order.id
        items.delete()

        return JsonResponse({'message': 'Order placed successfully','orderId':orderId})
    else:
        # Handle invalid request method (GET, etc.)
        return JsonResponse({'error': 'Invalid request method'})
    


def place_order(request, userId):   
    user_adds = UserAddress.objects.get(id=userId, user=request.user)
    cartss = Cart.objects.get(user=request.user)
    items = CartItems.objects.filter(cart=cartss)
    subtotal = items.aggregate(total_price=Sum('price'))['total_price'] or 0
    
    total_price = subtotal
    if cartss and cartss.coupons:
        coupon = get_object_or_404(Coupon, coupon_code=cartss.coupons)
        min_amount = coupon.discount_price
        total_price = subtotal - min_amount
    else:
        total_price = subtotal
    order = Order.objects.create(
        user=request.user,
        address=user_adds,
        total_price=total_price,
        payment_status='PENDING',
        payment_method='CASH_ON_DELIVERY',
    )
    coupon = get_object_or_404(Cart, user=request.user)
    coupon.coupons = None
    coupon.save()


    for cart_item in items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            price=cart_item.price,
            quantity=cart_item.quantity
        )
        print(order,"----------------")
        variant = cart_item.product
        variant.stock -= cart_item.quantity
        variant.save()

    # Fetch the updated order instance
   
    items.delete()
    itemss = OrderItem.objects.filter(order=order)
   
    context = {
        'items': itemss,
        'total_price': total_price,
        'orders': order
    }
    return render(request, "order/order_success.html", context)


def ordertable(request):
    order = Order.objects.filter(user=request.user).annotate(total_products=Sum('orderitem__quantity'))

    context = {
        'order':order
    }
    return render(request,'order/ordertable.html',context)

def order_view(request,order_id):
    orders = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=orders)
    total_price = sum(item.price * item.quantity for item in items)

    context = {
        'orders':orders,
        'items':items,
        'total_price':total_price
    }
   

    return render(request,"order/order_view.html",context)


def cancel_orderss(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    walletss = wallet.objects.get(user = request.user)
    
    if order.payment_status != 'CANCELLED':
        # Update the payment status to 'CANCELLED'
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
        
            print(item.quantity)
            variant = item.product  
            variant.stock += item.quantity
            variant.save()
          
        walletss.wallet_total += order.total_price
        print(walletss.wallet_total,"-------------------------")
        walletss.save()
        order.payment_status = 'CANCELLED'
        order.save()
        order_items.delete()

    return redirect('ordertable')



# views.py
def initiate_payment(request):
    if request.method == 'POST':
        # Retrieve the total price and other details from the backend
        cartss = Cart.objects.get(user=request.user)
        items = CartItems.objects.filter(cart=cartss)
    
        subtotal = items.aggregate(total_price=Sum('price'))['total_price'] or 0
        
        total_price = subtotal
        if cartss and cartss.coupons:
            coupon = get_object_or_404(Coupon, coupon_code=cartss.coupons)
            min_amount = coupon.discount_price
            total_price = subtotal - min_amount
        else:
            total_price = subtotal


        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create({

            'amount': int(total_price * 100),
              'currency': 'INR', 
              'payment_capture': 1
              
              })
       
    
        response_data = {
            'order_id': payment['id'],
            'amount': payment['amount'],
            'currency': payment['currency'],
            'key': settings.RAZOR_KEY_ID,

        }
        return JsonResponse(response_data)

    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})



def order_success(request,orderId):
    orders = Order.objects.get(id=orderId)
    items = OrderItem.objects.filter(order=orders)
    total_price = sum(item.price * item.quantity for item in items)

    context = {
        'orders':orders,
        'items':items,
        'total_price':total_price
    }


    return render(request,"order/order_success.html",context)