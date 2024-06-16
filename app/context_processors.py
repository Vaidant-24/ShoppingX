from app.models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_item_count = 0
    return {'cart_count': cart_item_count}
