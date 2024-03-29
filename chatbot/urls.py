from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name='main'),
    path("sign-up/", views.SignUp.as_view(), name='signup'),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.LoginView.as_view(), name="login"),
]