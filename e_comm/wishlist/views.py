from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from products.models import *
from .models import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def wishlist(request):
    
    product = whishlist.objects.filter(user = request.user)


    context = {
        'product':product
    }
    return render(request,"wishlist/wishlist.html",context)



def adding_wishlist(request):
    if request.method == 'POST':
   
        variant_id = request.POST.get('variant_id')
        try:
            variant = Variant.objects.get(id=variant_id)
        except Variant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid variant ID.'})

        # Check if the variant is not already in the wishlist for the current user
        if not whishlist.objects.filter(user=request.user, product=variant).exists():
            wishlist_item = whishlist.objects.create(user=request.user, product=variant)
            print('Item added to the wishlist:', wishlist_item)
            return JsonResponse({'status': 'success', 'message': 'Item added to the wishlist.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Item already in the wishlist.'})
    return JsonResponse({'status': 'error', 'message': 'Item already in the wishlist.'})


def removing_wishlist(request):
    if request.method == 'POST':
   
        variant_id = request.POST.get('variant_id')
        try:
            variant = Variant.objects.get(id=variant_id)
        except Variant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid variant ID.'})

        try:
            wishlist_item = whishlist.objects.get(user=request.user, product=variant)
            wishlist_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Item removed from the wishlist.'})
        except whishlist.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found in the wishlist.'})
      
    return JsonResponse({'status': 'error', 'message': 'Item not found in the wishlist.'})


def remove_item(request,variant_id):
   
    variant = Variant.objects.get(id=variant_id)
    print(variant_id,'-----------------------------')
 
    try:
        wishlist_item = whishlist.objects.get(user=request.user, product=variant)
        wishlist_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    except whishlist.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

 