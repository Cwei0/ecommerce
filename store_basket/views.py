from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from store.models import Product
from .basket import Basket


# Create your views here.
def basket_summary(request):
    return render(request, "store/basket/summary.html")


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, product_qty=product_qty)
        
        basket_qty = basket.__lens__()
        response = JsonResponse({"qty": basket_qty})
        return response
