from django import forms
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
        label="Enter Username",
        min_length=8,
        max_length=20,
        help_text="Required"
    )
    email = forms.EmailField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Please input your email"},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = UserBase
        fields = ("user_name", "email")
