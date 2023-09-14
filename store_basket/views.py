from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .basket import Basket
from store.models import Product


# Create your views here.
def basket_summary(request):
    return render(request, "store/basket/summary.html")


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        productid = int(request.POST.get("productid"))
        product = get_object_or_404(Product, id=productid)
        basket.add(product=product)
        response = JsonResponse({"test": "data"})
        return response
