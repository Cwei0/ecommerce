from django.test import TestCase

from ..models import Product, Category, User

class TestCategoriesModel(TestCase):
    """
    Test class for the Category model.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating a Category instance.
        """
        self.data1 = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        """
        Test if the data1 instance is an instance of the Category model.
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_return(self):
        """
        Test if the string representation of the data1 instance matches "django".
        """
        data = self.data1
        self.assertEqual(str(data), "django")


class TestProductsModel(TestCase):
    """
    Test class for the Product model.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by creating Category and User instances,
        and then creating a Product instance.
        """
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

    def test_products_model_entry(self):
        """
        Test if the data1 instance is an instance of the Product model.
        Test if the string representation of the data1 instance matches "django beginners".
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "django beginners")
