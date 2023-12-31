from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product
from unittest import skip

class TestBasketView(TestCase):
    def setUp(self):
        category = Category.objects.create(name="django", slug="django")
        user = User.objects.create(username="admin")
        self.product1 = Product.objects.create(
            title="django beginners",
            category=category,
            created_by=user,
            slug="django-beginners",
            price="20.00",
            image="django",
        )
        self.product2 = Product.objects.create(
            title="django intermediate",
            category=category,
            created_by=user,
            slug="django-beginners",
            price="20.00",
            image="django",
        )
        self.product3 = Product.objects.create(
            title="django advanced",
            category=category,
            created_by=user,
            slug="django-beginners",
            price="20.00",
            image="django",
        )
        self.client.post(
            reverse("store_basket:basket_add"),
            {"productid": self.product1.pk, "productqty": 1, "action": "post"},
            xhr=True,
        )
        self.client.post(
            reverse("store_basket:basket_add"),
            {"productid": self.product2.pk, "productqty": 2, "action": "post"},
            xhr=True,
        )

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse("store_basket:basket_summary"))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse("store_basket:basket_add"),
            {"productid": self.product3.pk, "productqty": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"qty": 4})
        response = self.client.post(
            reverse("store_basket:basket_add"),
            {"productid": self.product2.pk, "productqty": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"qty": 3})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse("store_basket:basket_delete"),
            {"productid": self.product2.pk, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"qty": 1, "subtotal": "20.00"})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse("store_basket:basket_update"),
            {"productid": self.product2.pk, "productqty": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"qty": 2, "subtotal": "40.00"})
