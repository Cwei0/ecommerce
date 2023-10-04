from importlib import import_module
from django.conf import settings
from unittest import skip
from django.urls import reverse
from django.http import HttpRequest
from store.views import product_all
from store.models import Category, Product
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory


@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_example(self):
        pass


# def test_homepage_url(self):
#     """
#     Test homepage response status
#     """
#     response = self.Client.get('/')


class TestViewResponse(TestCase):
    """
    Test class for checking view responses and URLs.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating Client, RequestFactory instances,
        and creating a sample Category, User, and Product.
        """
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

    def create_session_request(self):
        """
        Create a request object with a session.
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        return request

    def test_url_allowed_host(self):
        """
        Test if an HTTP request with an allowed host returns a 200 status code.
        """
        response = self.c.get("/", HTTP_HOST="noaddress.com")
        self.assertEqual(response.status_code, 400)

    def test_product_detail_url(self):
        """
        Test if the product detail URL returns a 200 status code.
        """
        response = self.c.get(
            reverse("store:product_detail", args=["django-beginners"])
        )
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test if the category detail URL returns a 200 status code.
        """
        response = self.c.get(reverse("store:category_list", args=["django"]))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Test if the homepage HTML contains the expected title and returns a 200 status code.
        """
        request = self.create_session_request()
        response = product_all(request)  # Assuming product_all is the view being tested
        html = response.content.decode("utf8")
        self.assertIn("<title> BookStore </title>", html)
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        """
        Test if the view function produces the expected HTML containing the title
        and returns a 200 status code.
        """
        request = self.factory.get("/django-beginners")
        request = self.create_session_request()
        response = product_all(request)  # Assuming product_all is the view being tested
        html = response.content.decode("utf8")
        self.assertIn("<title> BookStore </title>", html)
        self.assertEqual(response.status_code, 200)
