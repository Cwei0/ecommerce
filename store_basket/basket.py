from store.models import Product
from decimal import Decimal

class Basket:
    """
    A base Basket class for managing user shopping baskets.

    This class provides methods for adding, updating, deleting, and
    retrieving information about items in the shopping basket.

    Attributes:
        session (Session): The user's session object.
        basket (dict): A dictionary containing the user's shopping basket data.
    """

    def __init__(self, request):
        """
        Initialize a new Basket instance for a user.

        Args:
            request (HttpRequest): The HTTP request object.

        This constructor sets up the basket object for the current user's session.
        """
        self.session = request.session
        basket = self.session.get("skey")
        if "skey" not in request.session:
            basket = self.session["skey"] = {}
        self.basket = basket

    def add(self, product, product_qty):
        """
        Add a product in the shopping basket.

        Args:
            product (Product): The product to add.
            product_qty (int): The quantity of the product to add.

        This method adds the specified product in the user's basket session data.
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]["qty"] = int(product_qty)
        else:
            self.basket[product_id] = {
                "price": str(product.price),
                "qty": int(product_qty),
            }

        self.save()

    def get_total_price(self):
        """
        Calculate the total price of items in the shopping basket.

        Returns:
            Decimal: The total price of all items in the basket.
        """
        return sum(
            Decimal(item["price"]) * item["qty"] for item in self.basket.values()
        )

    def delete(self, product_id):
        """
        Delete a product from the shopping basket.

        Args:
            product_id: The ID of the product to delete from the basket.

        This method removes the specified product from the basket.
        """
        product_id = str(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product_id, product_qty):
        """
        Update the quantity of a product in the shopping basket.

        Args:
            product_id: The ID of the product to update.
            product_qty: The new quantity of the product.

        This method updates the quantity of the specified product in the basket.
        """
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = product_qty

        self.save()

    def __iter__(self):
        """
        Iterate over items in the basket and retrieve associated product data.

        Yields:
            dict: A dictionary containing information about each item in the basket.
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Get the total quantity of items in the shopping basket.

        Returns:
            int: The total quantity of items in the basket.
        """
        return sum(item["qty"] for item in self.basket.values())

    def save(self):
        """
        Mark the session as modified to ensure changes are saved.

        This method sets the 'modified' flag on the session to ensure that changes
        made to the basket are saved to the session data.
        """
        self.session.modified = True
