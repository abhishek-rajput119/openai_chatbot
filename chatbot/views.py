from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, redirect
from django.views.generic import CreateView, FormView
from django.contrib import messages
from os import getenv
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from chatbot.forms import SignUpForm, UserLoginForm
from chatbot.models import Chat
import openai
from openai import OpenAI

client = OpenAI(
    api_key=getenv("OPENAI_API_KEY"),
)

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                user_input = request.POST.get('userInput')

                clean_user_input = str(user_input).strip()

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": clean_user_input,
                        }
                    ],
                )
                # get response

                bot_response = response.choices[0].message.content

                obj, created = Chat.objects.get_or_create(
                    user=request.user,
                    messageInput=clean_user_input,
                    bot_response=bot_response,
                )
            except openai.APIConnectionError as e:
                messages.warning(request, f"Failed to connect to OpenAI API")
            except openai.RateLimitError as e:
                messages.warning(request, f"You exceeded your current quota.")
            except openai.AuthenticationError as e:
                messages.warning(request, f"Incorrect API key provided.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            # retrieve all messages belong to logged in user
            get_history = Chat.objects.filter(user=request.user)
            context = {'get_history': get_history}
            return render(request, 'index.html', context)
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
