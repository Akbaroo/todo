from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control mb-3"

        self.fields["username"].widget.attrs.update({"placeholder": "نام کاربری"})
        self.fields["email"].widget.attrs.update({"placeholder": "ایمیل"})
        self.fields["password1"].widget.attrs.update({"placeholder": "گذرواژه"})
        self.fields["password2"].widget.attrs.update({"placeholder": "تأیید گذرواژه"})


class EmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل خود را وارد کنید.")

    email.widget.attrs.update(
        {"class": "form-control mb-3", "placeholder": "آدرس ایمیل"}
    )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "نام کاربری"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "گذرواژه"}
        )
