import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from cart.models import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail,EmailMessage
from e_comm import settings
# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def address(request):
    cart = get_object_or_404(Cart, user=request.user)
    cartitems = CartItems.objects.filter(cart = cart)
    if cartitems:

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
    
    return redirect('shop',0)

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



def password_reset(request):
        if request.method == 'POST':
            pass1 = request.POST.get('pass1')
            newpassword1 = request.POST.get('newpass1')
            newpassword2 = request.POST.get('newpass2')

            user = request.user
            

            if newpassword1 == newpassword2:
                # Use regex to check password criteria
                if re.match(r'^(?=.*[a-z])(?=.*\d)(?!.*\s)[A-Za-z\d]{8,}$', newpassword1):
                    if user.check_password(pass1):
                        user.password = make_password(newpassword1)
                        user.save()
                        user = authenticate(username=user.username, password=pass1)
                        login(request, user)
                        subject = "Password Changed"
                        message = """
Your password has been successfully changed. If you did not perform this action, please contact our support team immediately.

"""
                        from_email = settings.EMAIL_HOST_USER
                        print( from_email,'>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<')
                        email_user = request.user
                        print(email_user.email,'>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<')
                        to_list = [email_user.email]
                        send_mail(subject, from_email,message,to_list, fail_silently = True )
                       
                        messages.success(request, 'Password reset successful!')
                        return HttpResponseRedirect('profile_view')
                    else:
                        messages.error(request, 'Current password is incorrect.')
                else:
                    messages.error(request, 'New password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one digit.')
            else:
                messages.error(request, 'New passwords do not match.')
       
            
        return render(request,'profile/reset_password.html')

