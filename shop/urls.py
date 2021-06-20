"""Enter your URL patterns here"""

from django.urls import path, include

from . import views


app_name = "shop"


urlpatterns = [
    path("", views.category_list, name="category_list"),
    path("<slug:category_slug>/", views.category_list,
         name="category_list_by_product"),
    path("<int:id>/<slug:product_slug>/", views.product_info,
         name="product_info"),
]
