class Basket:
    """
    A base Basket class, providing some default behaviours
    that can be inherited or overrided, if necessary
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get("skey")
        if "skey" not in request.session:
            basket = self.session["skey"] = {}
        self.basket = basket

    def add(self, product, product_qty):
        """
        Adding and updating the user's basket session data
        """
        product_id = product.id
        if product_id not in self.basket:
            self.basket[product_id] = {"price": str(product.price), "qty": int(product_qty)}

        self.session.modified = True

    def __lens__(self):
        """
        Get the basket data and count the quantity of items
        """
        return sum(item["qty"] for item in self.basket.values())