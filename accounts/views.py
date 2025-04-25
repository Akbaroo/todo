import string
import random

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site

from .forms import CustomUserCreationForm, LoginForm, EmailForm

User = get_user_model()


def next_url(request):
    """Return the 'next' URL from GET parameters or '/' as fallback."""
    return request.GET.get("next", "/")


def generate_verification_token():
    """Generate a random token for email verification."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=64))


def signup_view(request):
    """Handle user signup process."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # After successful signup, redirect to email verification step
            return redirect(reverse("auth:send_email_verify") + f"?next={next_url(request)}")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


def send_email_verify(request):
    """Send email to user for verifying their email address."""
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Handle case where email is not found in the database
                messages.warning(request, "ایمیل وارد شده اشتباه است یا شما هنوز ثبت‌نام نکرده‌اید.")
                return redirect(next_url(request))

            if user.is_verified:
                # If email is already verified, inform the user
                messages.info(request, "ایمیل شما قبلاً تأیید شده است.")
                return redirect(reverse("auth:login"))

            # Generate a verification token and save it to the user's profile
            verification_token = generate_verification_token()
            user.verification_token = verification_token
            user.save()

            # Send the verification email
            current_site = get_current_site(request)
            scheme = 'https' if request.is_secure() else 'http'
            verify_url = f"{scheme}://{current_site.domain}{reverse('auth:email_verify', args=[verification_token])}"

            from_email = settings.DEFAULT_FROM_EMAIL
            to = [user.email]
            context = {
                "user": user,
                "domain": current_site.domain,
                "token": verification_token,
                "verify_url": verify_url,
            }

            # Render HTML message and prepare the plain text message
            html_message = render_to_string("registration/verification_email.html", context)
            text_message = f"سلام {user.username} عزیز، لطفاً روی لینک زیر کلیک کنید تا ایمیل خود را تأیید کنید:\n\n{verify_url}"

            # Send the email with both HTML and plain text alternatives
            msg = EmailMultiAlternatives("تأیید ایمیل شما", text_message, from_email, to)
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            # Inform the user to check their email
            messages.warning(request, "ایمیل تأیید ارسال شد. لطفاً صندوق ورودی ایمیل خود را بررسی کنید.")
            return redirect(reverse("blog:home") + f"?next={next_url(request)}")

    else:
        form = EmailForm()

    return render(request, "registration/send_email_verify.html", {"form": form})


def email_verify(request, token=None):
    """Verify the user's email address using the token sent in the email."""
    try:
        user = User.objects.get(verification_token=token)
    except User.DoesNotExist:
        # If the token is invalid or expired, raise a 404 error
        raise Http404("توکن نامعتبر است")

    # Mark user as verified and clear the verification token
    user.is_verified = True
    user.verification_token = ""
    user.save()

    return redirect(reverse("auth:login") + f"?next={next_url(request)}")


class LoginView(auth_views.LoginView):
    """Custom login view that checks if the user's email is verified."""
    form_class = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_verified:
            # Log the user out if their email is not verified and show a warning
            logout(self.request)
            messages.warning(self.request, "لطفاً ابتدا ایمیل خود را تأیید کنید.")
            messages.warning(
                self.request,
                f"برای تأیید ایمیل، به <a href='{reverse('auth:send_email_verify')}'>این لینک</a> بروید.",
            )
            return redirect("home")

        return super().form_valid(form)


def logout_view(request):
    """Log the user out and redirect to the next URL."""
    logout(request)
    messages.info(request, "شما از حساب کاربری خود خارج شدید.")
    return redirect(next_url(request))