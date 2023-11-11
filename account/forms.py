from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import UserBase


class RegistrationForm(forms.ModelForm):
    """
    A form for user registration.

    This form is used to collect user registration information, including username, email,
    password, and password confirmation.

    Attributes:
        user_name (CharField): The username input field.
        email (EmailField): The email input field.
        password (CharField): The password input field.
        confirm_password (CharField): The password confirmation input field.

    Meta:
        model (UserBase): The model associated with the form.
        fields (tuple): The fields to include in the form.
    """

    user_name = forms.CharField(
        label="Enter Username", min_length=8, max_length=20, help_text="Required"
    )
    email = forms.EmailField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Please input your email"},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput
    )

    class Meta:
        model = UserBase
        fields = ("user_name", "email")

    def clean_username(self):
        user_name = self.cleaned_data["user_name"].lower()
        user = UserBase.objects.filter(user_name=user_name)
        if user.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password(self):
        cleaned_data = self.cleaned_data
        if cleaned_data["password"] != cleaned_data["confirm_password"]:
            raise forms.ValidationError("Password do not match")
        return cleaned_data["password"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Please use another email, that is already taken"
            )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Username"}
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control mb-3",
                "placeholder": "E-mail",
                "name": "email",
                "id": "id_email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Password"}
        )
        self.fields["confirm_password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat Password"}
        )
