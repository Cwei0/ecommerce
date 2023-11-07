from django.urls import path
from .views import user_registration

app_name = "account"

urlpatterns = [
    path("register/", user_registration, name="register"),
]
