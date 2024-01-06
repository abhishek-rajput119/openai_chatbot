from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, redirect
from django.views.generic import CreateView, FormView
from django.contrib import messages

from chatbot.forms import SignUpForm, UserLoginForm


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect("login")

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "register.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.warning(self.request, f"{field}: {error}")
        return redirect(self.request.META['HTTP_REFERER'])

    def get_success_url(self):
        return reverse("main")


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = "login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, "You are logged in")
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.warning(self.request, f"{error}")
        return redirect(self.request.META['HTTP_REFERER'])

    def get_success_url(self):
        return reverse("main")


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("main")
