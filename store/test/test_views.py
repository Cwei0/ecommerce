from unittest import skip
from django.urls import reverse
from django.http import HttpRequest
from store.views import all_products
from store.models import Category, Product
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory


# @skip("demonstrating skipping")
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass

# def test_homepage_url(self):
#     """
#     Test homepage response status
#     """
#     response = self.Client.get('/')


class TestViewResponse(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        self.factory = RequestFactory()
        category = Category.objects.create(name="django", slug="django")
        user = User.objects.create(username="admin")
        self.data1 = Product.objects.create(
            title="django beginners",
            category=category,
            created_by=user,
            slug="django-beginners",
            price="20.00",
            image="django",
        )

    def test_url_allowed_host(self):
        """
        Test allowed host
        """
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(
            reverse("store:product_detail", args=["django-beginners"])
        )
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        response = self.c.get(reverse("store:category_list", args=["django"]))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = all_products(request)
        html = response.content.decode('utf8')
        print(html)
        self.assertIn('<title> Home </title>', html)
        self.assertEqual(response.status_code, 200)

    
    def test_view_function(self):
        request = self.factory.get('/item/django-beginners')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title> Home </title>', html)
        self.assertEqual(response.status_code, 200)
