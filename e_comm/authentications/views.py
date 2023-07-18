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


def home(request):
   if request.user.is_authenticated:
      product =  Products.objects.all()
      
      paginator = Paginator(product, 5)  # Display 3 products per page
  
      page_number = request.GET.get('page')
      products = paginator.get_page(page_number)

   
      cat = Category.objects.all()
   
      context = {
        'products':products
        ,'cat':cat
        }

      
      return render(request, 'verify/home1.html', context)
   else:

      return render(request, 'verify/home1.html')

def signin(request):
 
   
   if request.method == 'POST':
      username = request.POST["username"]
      pass1 = request.POST['pass1']

      user = authenticate(username = username, password = pass1)

      if user is not None :
        
         otp_store = get_random_string(length=5, allowed_chars='0123456789')
         request.session['otp'] = otp_store
         request.session['user_pk'] = user.pk
         subject = "OTP confirmations"
         print(otp_store,"--------------otp===================")
         message = f"Your otp is{otp_store}"
         from_email = settings.EMAIL_HOST_USER
         to_list = [user.email]
         send_mail(subject, from_email,message,to_list, fail_silently = True )
         # login(request,user)
         # return redirect('home')

         return render(request,'verify/otp_login.html')
      else :
         messages.error(request, "username or password incorrect")  
         return redirect('signin')
      
      
   return render(request,'verify/sigin.html')

def signup(request):
   if request.method == 'POST' :
      username = request.POST['username']
      email = request.POST['email']
      pass1 = request.POST['pass1']
      pass2 = request.POST['pass2']
      myuser = User.objects.create_user(username,email,pass1)
      myuser.is_active = False
      myuser.save()



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
    

   return render(request,'verify/signup.html')

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
