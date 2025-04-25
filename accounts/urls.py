from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path("send-email/", views.send_email_verify, name="send_email_verify"),
    path("verify-email/<str:token>/", views.email_verify, name="email_verify"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]