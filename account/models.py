from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class CustomAccountManager(BaseUserManager):
    """
    A custom manager for the UserBase model, providing methods for creating superusers and regular users.
    """

    def create_superuser(self, email, user_name, password, **other_fields):
        """
        Create and return a superuser with the given email, user_name, and password.

        Args:
            email (str): The email address of the superuser.
            user_name (str): The username of the superuser.
            password (str): The password for the superuser.
            **other_fields: Additional fields for the superuser.

        Returns:
            UserBase: The created superuser instance.
        
        Raises:
            ValueError: If is_staff or is_superuser is not set to True.
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")
        
        return self.create_user(email, user_name, password, **other_fields)
    
    def create_user(self, email, user_name, password, **other_fields):
        """
        Create and return a regular user with the given email, user_name, and password.

        Args:
            email (str): The email address of the user.
            user_name (str): The username of the user.
            password (str): The password for the user.
            **other_fields: Additional fields for the user.

        Returns:
            UserBase: The created user instance.
        
        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class UserBase(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model representing user accounts with extended profile information.
    """

    email = models.EmailField(_("email address"), max_length=254, unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150, unique=True)
    about = models.TextField(_("about"), max_length=500, blank=True)

    # Delivery Details
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)

    # User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        """
        Return the username as the string representation of the user.

        Returns:
            str: The username.
        """
        return self.user_name
