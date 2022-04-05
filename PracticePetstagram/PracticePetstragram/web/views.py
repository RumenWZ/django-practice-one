from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

# Create your views here.
from PracticePetstragram.accounts.models import Profile
from PracticePetstragram.web.forms import CreateProfileForm
from PracticePetstragram.web.models import Pet, PetPhoto


class HomeView(views.TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['hide_additional_nav_items'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(views.TemplateView):
    template_name = 'dashboard.html'


