
from django import template
from cart.models import CartItems
from wishlist.models import whishlist

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_items_count(context):
    user = context['request'].user
    cart_items_count = CartItems.objects.filter(cart__user=user).count()
    return cart_items_count

@register.simple_tag(takes_context=True)
def whishlist_count(context):
    user = user = context['request'].user
    whishlist_count = whishlist.objects.filter(user = user).count()
    return whishlist_count  - 1

@register.filter
def in_wishlist(user, product_id):
    
    return whishlist.objects.filter(user=user, product__id=product_id).exists()

@register.simple_tag(takes_context=True)
def is_active(context, url_name):
    # Get the current request object from the context
    request = context['request']
    
    # Check if the given URL name matches the view name of the current URL
    if request.resolver_match.view_name == url_name:
        return 'active'
    return ''



