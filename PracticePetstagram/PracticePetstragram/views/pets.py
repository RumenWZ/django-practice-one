from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic as views

from PracticePetstragram.web.forms import CreatePetForm, EditPetForm, DeletePetForm


class CreatePetView(LoginRequiredMixin, views.CreateView):
    form_class = CreatePetForm
    template_name = 'pet_create.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):               #if user missing in __init__ do this
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditPetView(LoginRequiredMixin, views.UpdateView):
    form_class = EditPetForm
    template_name = 'pet_edit.html'


class DeletePetView(LoginRequiredMixin, views.DeleteView):
    form_class = DeletePetForm
    template_name = 'pet_delete.html'