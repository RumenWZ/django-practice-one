from django.urls import reverse_lazy
from django.views import generic as views

from PracticePetstragram.web.models import PetPhoto


class PetPhotoDetailsView(views.DetailView):
    model = PetPhoto
    template_name = 'photo_details.html'
    context_object_name = 'pet_photo'

    def get_queryset(self):
        queryset = super().queryset()
        queryset.prefetch_related('tagged_pets')
        return queryset


class PetPhotoCreateView(views.CreateView):
    model = PetPhoto
    template_name = 'photo_create.html'
    fields = ('photo', 'description', 'tagged_pets')
    success_url = reverse_lazy('dashboard')



class PetPhotoEditView(views.UpdateView):
    pass