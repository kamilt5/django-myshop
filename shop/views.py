from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from cart.forms import CartForm

# Create your views here.


def category_list(request, category_slug=None):
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
    else:
        category = None
        products = Product.objects.filter(available=True)

    return render(request, "shop/products/category.html",
                  context={"category": category, 
                           "products": products,
                           "categories": categories})


def product_info(request, id, product_slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=product_slug,
                                available=True,
                                )
    cart_form = CartForm()

    return render(request, "shop/products/product.html",
                  context={"product": product,
                           "cart_form": cart_form})
