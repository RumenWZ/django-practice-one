from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from PracticePetstragram.web.models import PetPhoto


class PetPhotoDetailsView(views.DetailView):
    model = PetPhoto
    template_name = 'photo_details.html'
    context_object_name = 'pet_photo'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        viewed_pet_photos = request.session.get('last_viewed_pet_photo_ids', [])

        viewed_pet_photos.insert(0, self.kwargs['pk'])
        request.session['last_viewed_pet_photo_ids'] = viewed_pet_photos[:4]

        return response

    def get_queryset(self):
        return super() \
            .get_queryset() \
            .prefetch_related('tagged_pets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.object.user == self.request.user

        return context


class PetPhotoCreateView(views.CreateView):
    model = PetPhoto
    template_name = 'photo_create.html'
    fields = ('photo', 'description', 'tagged_pets')
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PetPhotoEditView(views.UpdateView):
    model = PetPhoto
    template_name = 'photo_edit.html'
    fields = ('description',)

    def get_success_url(self):
        return reverse_lazy('photo details', kwargs={'pk': self.object.id})


def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()

    return redirect('pet photo details', pk)