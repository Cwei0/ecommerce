from django.shortcuts import render, redirect, HttpResponse
from django.contrib.sites import shortcuts
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .forms import RegistrationForm
from .token import account_activation_token


# Create your views here.
def user_registration(request):
    # Check if user is already authenticated (logged in).
    # if request.user.is_authenticated:
    #     return redirect(
    #         ""
    #     )  # Redirect to the home page if the user is already logged in.

    if request.method == "POST":
        # Create an instance of the RegistrationForm and populate it with the data from the request.
        register_form = RegistrationForm(request.POST)

        # Check if the form is valid (i.e., all required fields are filled correctly).
        if register_form.is_valid():
            # Create a new UserBase instance but don't save it to the database yet.
            user = register_form.save(commit=False)

            # Assign the email and hashed password from the form data to the user object.
            user.email = register_form.cleaned_data["email"]
            user.set_password(register_form.cleaned_data["password"])

            # Set the user's account status to inactive until email confirmation.
            user.is_active = False

            # Save the user object to the database.
            user.save()

            # Get the current site information.
            current_site = shortcuts.get_current_site(request)

            # Prepare an email to send for account activation.
            subject = "Activate your account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            # Send the activation email to the user.
            user.email_user(subject=subject, message=message)

            # Send a Http responce to the UI to confirm activation mail sent
            return HttpResponse("Registered successfully and activation sent")

    else:
        register_form = RegistrationForm()
    return render(
        request, "account/registration/register.html", {"form": register_form}
    )


