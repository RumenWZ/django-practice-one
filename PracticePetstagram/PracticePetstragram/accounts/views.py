from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, login
from django.views import generic as views

# Create your views here.
from django.urls import reverse_lazy

from PracticePetstragram.accounts.models import Profile
from PracticePetstragram.common.view_mixins import RedirectToDashboard
from PracticePetstragram.web.forms import CreateProfileForm
from PracticePetstragram.web.models import Pet, PetPhoto


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
    success_url = reverse_lazy('dashboard')


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pets = list(Pet.objects.filter(user_id=self.object.user_id))

        pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()

        total_likes_count = sum(pp.likes for pp in pet_photos)
        total_pet_photos_count = len(pet_photos)

        context.update({
            'total_likes_count': total_likes_count,
            'total_pet_photos_count': total_pet_photos_count,
            'is_owner': self.object.user_id == self.request.user.id,
            'pets': pets,
        })

        return context

class ChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'