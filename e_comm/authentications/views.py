from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control,never_cache
from e_comm import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from .tokens import generate_token
import random
from django.utils.crypto import get_random_string        
from products.models import *      
from django.core.paginator import Paginator
from userprofile.models import Referral, generate_referral_code
from banners.models import Banner
from userorder.models import *
from django.db.models import Count

def is_valid_password(password):
   
    if len(password) < 8:
        return False

    # Check if the password contains at least one uppercase letter, one lowercase letter, and one digit
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False

    # Check if the password contains spaces
    if ' ' in password:
        return False

    return True



def home(request):
   if request.user.is_authenticated:
      products = Products.objects.all()
      orders = OrderItem.objects.values('product').annotate(order_count=Count('product'))

      # Create a dictionary to store product IDs and their order counts
      product_order_count = {item['product']: item['order_count'] for item in orders}

      # Sort products based on order count (most-sold first)
      trending_products = sorted(products, key=lambda p: product_order_count.get(p.id, 0), reverse=True)

      paginator = Paginator(trending_products, 4)  # Display 8 products per page
      page_number = request.GET.get('page')
      products = paginator.get_page(page_number)

      cat = Category.objects.all()
      banners = Banner.objects.all()
      context = {
         'products': products,
         'cat': cat,
         'banners': banners
      }

            
      return render(request, 'verify/home1.html', context)
   else:
      products = Products.objects.all()
      orders = OrderItem.objects.values('product').annotate(order_count=Count('product'))

      # Create a dictionary to store product IDs and their order counts
      product_order_count = {item['product']: item['order_count'] for item in orders}

      # Sort products based on order count (most-sold first)
      trending_products = sorted(products, key=lambda p: product_order_count.get(p.id, 0), reverse=True)

      paginator = Paginator(trending_products, 4)  # Display 8 products per page
      page_number = request.GET.get('page')
      products = paginator.get_page(page_number)

      cat = Category.objects.all()
      banners = Banner.objects.all()
      context = {
         'products': products,
         'cat': cat,
         'banners': banners
      }

            
      return render(request, 'verify/home1.html',context)

def signin(request):
   if request.user.is_authenticated:
       
       return redirect('home')
   
   if request.method == 'POST':
      username = request.POST["username"]
      pass1 = request.POST['pass1']

      user = authenticate(username = username, password = pass1)

      if user is not None :
        
         otp_store = get_random_string(length=5, allowed_chars='0123456789')
         request.session['otp'] = otp_store
         request.session['user_pk'] = user.pk
         esubject = "OTP Login"
         emessage = render_to_string('verify/otp_mail.html',{
         'name':user.username,
         'otp': otp_store,
      })
         email = EmailMessage(
            esubject,
            emessage,
            settings.EMAIL_HOST_USER,
            [user.email],

         )
         email.fail_silently = True
         email.send()
         
         return render(request,'verify/otp_login.html')
      else :
         messages.error(request, "username or password incorrect")  
         return redirect('signin')
      
      
   return render(request,'verify/sigin.html')


def signup(request):
   if request.user.is_authenticated:
       
       return redirect('home')
   if request.method == 'POST' :
      username = request.POST['username']
      email = request.POST['email']
      pass1 = request.POST['pass1']
      pass2 = request.POST['pass2']
      referral_code = request.POST.get('referal_code', None)
      
      if pass1 != pass2:
         messages.error(request, "Passwords do not match.")
         return redirect('signup')

      if User.objects.filter(username=username).exists():
         messages.error(request, "Username already exists.")
         return redirect('signup')

      # if User.objects.filter(email=email).exists():
      #    messages.error(request, "Email already registered.")
      #    return redirect('signup')
      if not is_valid_password(pass1):
         messages.error(request, "Password must be at least 8 characters long and contain one uppercase letter, one lowercase letter, and one digit.")
         return redirect('signup')
      if referral_code:
         try:
            referal = Referral.objects.get(referral_code = referral_code)
            referred_by_user = referal.user
         except User.DoesNotExist:
            messages.error(request, "Invalid referral code.")
            return redirect('signup')

# Create the user
      myuser = User.objects.create_user(username=username, email=email, password=pass1)
      myuser.is_active = False
      myuser.save()
      refferal_codes = Referral.objects.get(user =myuser)
      


      if referral_code:
       
         refferal_codes.referred_by = referred_by_user
         refferal_codes.save()
  
      else:
        
         refferal_codes.referred_by = None
         refferal_codes.save()

# send email to confirm 
     
      
      current_site = get_current_site(request)
      esubject = "confirm your email @ trejnexsus"
      emessage = render_to_string('verify/email_confirm.html',{
         'name':myuser.username,
         'domain': current_site.domain,
         'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
         'token':generate_token.make_token(myuser),
      })
      email = EmailMessage(
         esubject,
         emessage,
         settings.EMAIL_HOST_USER,
         [myuser.email],

      )
      email.fail_silently = True
      email.send()
      messages.success(request, "An link has been sent to your email so please go to the email and click the link give in that")
      return redirect('sendmail')
   return render(request,'verify/signup.html')

def sendmail(request):

   return render(request, 'verify/email_send.html')

def activate(request, uidb64, token):
   
    try:
      uid = force_str(urlsafe_base64_decode(uidb64))
      myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
      myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
      myuser.is_active = True
      myuser.save()
      login(request, myuser)
      
      return redirect('home')
    else:
      return render(request, 'verify/activation_failed.html')
   
   
def verifyotp(request):
    if request.method == 'POST':
        send_otp = request.session.get('otp')
        user_id = request.session.get('user_pk')
        store_otp = request.POST['fotp']

        if send_otp == store_otp:
            myuser = User.objects.get(id=user_id)
            login(request, myuser)
            return redirect('home')
        else:
            return redirect('signin')


def forget_password(request):
   if request.user.is_authenticated:
      
      return redirect('home')
   if request.method == 'POST' :
      username = request.POST['username']
      user = User.objects.get(username = username)
      current_site = get_current_site(request)
      esubject = "confirm your email @ trejnexsus"
      emessage = render_to_string('verify/pass_verify.html',{
         'name':user.username,
         'domain': current_site.domain,
         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
         'token':generate_token.make_token(user),
      })
      email = EmailMessage(
         esubject,
         emessage,
         settings.EMAIL_HOST_USER,
         [user.email],

      )
      email.fail_silently = True
      email.send()

      messages.success(request, "An link has been sent to your email so please go to the email and click the link give in that")
      return redirect('sendmail')
   
   return render(request,'verify/forget_password.html')
    
def reset_password(request, uidb64, token):
   
    try:
      uid = force_str(urlsafe_base64_decode(uidb64))
      myuser = User.objects.get(pk=uid)
      request.session['user_pk'] = myuser.pk
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
      myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
      myuser.is_active = True
      myuser.save()
      return redirect('update_password')
    else:
      return render(request, 'verify/activation_failed.html')

def update_password(request):
   user_id = request.session.get('user_pk')
   if request.method == 'POST':
      pass1 = request.POST['pass1']
      user = User.objects.get(pk=user_id)
      new_password = pass1
      user.set_password(new_password)
      username = user.username
      user.save()
      user = authenticate(username=username, password=pass1)
      login(request, user)
      return redirect('home')
   else:
      return render(request, 'verify/reset_password.html')

      
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
  
    # messages.success(request,"logged Out Successfully")
    return redirect('signin')
