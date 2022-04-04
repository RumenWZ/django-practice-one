from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, login
from django.views import generic as views

# Create your views here.
from django.urls import reverse_lazy

from PracticePetstragram.common.view_mixins import RedirectToDashboard
from PracticePetstragram.web.forms import CreateProfileForm


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserRegisterView(RedirectToDashboard, views.CreateView):
    form_class = CreateProfileForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('dashboard')

class UserLogoutView(auth_views.LogoutView):
    pass

