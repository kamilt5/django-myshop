from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from . import forms
from .cart import Cart


# Create your views here.

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = forms.CartForm(request.POST)
    if form.is_valid():
        print("yes")
        cd = form.cleaned_data
        cart.add(item=product, quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = forms.CartForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(request, 'cart/detail.html', context={"cart": cart})
