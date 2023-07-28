from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from cart.models import *

# Create your views here.

def address(request):
    wallets = wallet.objects.get(user = request.user)
  
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
    user_add = request.user
    address = UserAddress.objects.filter(user = user_add)
    context = {
        'cart':cart,
        'subtotal': subtotal,
        'total_price': total_price,
         'address':address,
    }

   

 
 
    return render(request,'address/address.html',context) 

def add_address(request):
    if request.method == 'POST':
        # Get form data from the request
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address_line_1 = request.POST.get('address1')
        address_line_2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('pincode')
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')

        # Create a new UserAddress object and save it to the database
        user_address = UserAddress(
            user=request.user,  # Assuming the request has a logged-in user
            first_name=first_name,
            last_name=last_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            email=email,
            phone_number=phone_number
        )
        user_address.save()
        return redirect('address')
    return render(request,'address/add_address.html')

def edit_address(request,address_id):
     try:
        user_address = UserAddress.objects.get(id=address_id, user=request.user)
     except UserAddress.DoesNotExist:
        return HttpResponse('Address not found.')
     if request.method == 'POST':
        # Get form data from the request
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address_line_1 = request.POST.get('address1')
        address_line_2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('pincode')
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')

        # Update the user address fields
        user_address.first_name = first_name
        user_address.last_name = last_name
        user_address.address_line_1 = address_line_1
        user_address.address_line_2 = address_line_2
        user_address.city = city
        user_address.state = state
        user_address.postal_code = postal_code
        user_address.country = country
        user_address.email = email
        user_address.phone_number = phone_number

        # Save the updated user address
      
        user_address.save()
        return redirect('address')
     context = {
         'user_address':user_address
     }
     return render(request,'address/edit_address.html',context)

def profile_view(request):
     if request.method == 'POST':
        # Get the form data from the request
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Update the user object with the new information
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        
        return redirect('profile_view')  # Redirect to the profile view or any other desired page after updating
   
     return render(request,'profile/profile.html')


def user_address(request):
    user_add = request.user
    address = UserAddress.objects.filter(user = user_add)
    context = {
        'address':address
    }
    return render(request,'address/address.html',context) 

def test(request):
    refferal = Referral.objects.get(user = request.user)
    wallets = wallet.objects.get(user=request.user)
    user = Referral.objects.filter(referred_by = request.user)
    context ={
        'user':user,
        'offers':refferal,
        'wallets':wallets    
        }
    return render(request,"profile/offers.html",context)

def profile_address(request):
    user_add = request.user
    address = UserAddress.objects.filter(user = user_add)
    
    if request.method == 'POST':
        # Get form data from the request
        print('evideo000000000000')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address_line_1 = request.POST.get('address1')
        address_line_2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('pincode')
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')

        # Create a new UserAddress object and save it to the database
        UserAddress.objects.create(
            user=request.user,  # Assuming the request has a logged-in user
            first_name=first_name,
            last_name=last_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            email=email,
            phone_number=phone_number
        )
     
        return redirect('profile_address')
    context = {
        'address':address
    }
    return render(request,'profile/user_address.html',context) 


def delete_address(request,add_userId):
    user_address = UserAddress.objects.get(id=add_userId)
    user_address.is_active = False
    user_address.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 



def edit_profile_address(request,address_id):
     try:
        user_address = UserAddress.objects.get(id=address_id, user=request.user)
     except UserAddress.DoesNotExist:
        return HttpResponse('Address not found.')
     if request.method == 'POST':
        # Get form data from the request
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address_line_1 = request.POST.get('address1')
        address_line_2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('pincode')
        country = request.POST.get('country')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')

        # Update the user address fields
        user_address.first_name = first_name
        user_address.last_name = last_name
        user_address.address_line_1 = address_line_1
        user_address.address_line_2 = address_line_2
        user_address.city = city
        user_address.state = state
        user_address.postal_code = postal_code
        user_address.country = country
        user_address.email = email
        user_address.phone_number = phone_number

        # Save the updated user address
      
        user_address.save()
        return redirect('profile_address')
     context = {
         'user_address':user_address
     }
     return render(request,'profile/edit_user_address.html',context)
