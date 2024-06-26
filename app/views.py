from django.shortcuts import render,redirect
from django.views import View
from app.models import Customer,Product,OrderPlaced,Cart
from app.forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form, 'active': 'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
        messages.success(request, "Congratulations! your profile saved successfully")
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category = 'TW')
        bottomwears = Product.objects.filter(category = 'BW')
        mobiles = Product.objects.filter(category = 'M')
        
        return render(request, 'app/home.html', {'topwears': topwears,'bottomwears': bottomwears,'mobiles':mobiles})


class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already = False
        if request.user.is_authenticated:
            item_already = Cart.objects.filter(Q(user = request.user) & Q(product = product.id)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_already':item_already})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    reg = Cart(user = user, product = product)
    reg.save()
    return redirect('/cart')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shippingAmount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempAmount = (p.quantity * p.product.discount_price)
            amount += tempAmount
            totalAmount = amount + shippingAmount
            
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalAmount': totalAmount,
        }
        return JsonResponse(data)

@login_required    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shippingAmount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempAmount = (p.quantity * p.product.discount_price)
            amount += tempAmount
            totalAmount = amount + shippingAmount
            
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalAmount': totalAmount,
        }
        return JsonResponse(data)
    
@login_required    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        rem = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        rem.delete()
        
        amount = 0.0
        shippingAmount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempAmount = (p.quantity * p.product.discount_price)
            amount += tempAmount
        totalAmount = amount + shippingAmount
        
        data = {
            'amount': amount,
            'totalAmount': totalAmount,
            'cart_empty': len(cart_product) == 0
        }
        return JsonResponse(data)

def empty_cart(request):
    return render(request, 'app/emptycart.html')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        amount = 0.0
        totalAmount = 0.0
        shippingAmount = 70.0
        
        if cart_product:
            for p in cart_product:
                tempAmount = (p.quantity * p.product.discount_price)
                amount += tempAmount
                totalAmount = amount + shippingAmount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totalAmount':totalAmount, 'amount':amount})
        else:
            return render(request,'app/emptycart.html')
    

@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def profile(request):
    return render(request, 'app/profile.html')

@login_required
def address(request):
    addr = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html',{'addr':addr,'active':'btn-primary'})

def mobile(request,data = None):
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'OnePlus' or data == 'Samsung':
        mobiles = Product.objects.filter(category = 'M').filter(brand = data)
    elif data == 'Above':
        mobiles = Product.objects.filter(category = 'M').filter(discount_price__gt=25000)
    elif data == 'Below':
        mobiles = Product.objects.filter(category = 'M').filter(discount_price__lt=25000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! You are registered successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    add = Customer.objects.filter(user = request.user)
    cart_items = Cart.objects.filter(user = request.user)
    amount = 0.0
    shippingAmount = 70.0
    totalAmount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempAmount = (p.quantity * p.product.discount_price)
            amount += tempAmount
        totalAmount = amount + shippingAmount
    return render(request, 'app/checkout.html', {'add' : add, 'totalAmount' : totalAmount, 'cart_items' :cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user = user, product = c.product, customer = customer, quantity = c.quantity).save()
        c.delete()
    return redirect('orders')
    
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html',{'orders':op})

