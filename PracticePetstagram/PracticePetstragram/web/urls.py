from django.urls import path
from django.views.generic import TemplateView

from PracticePetstragram.views.pet_photo import PetPhotoDetailsView, PetPhotoCreateView, like_pet_photo, \
    PetPhotoEditView
from PracticePetstragram.views.pets import CreatePetView, EditPetView, DeletePetView
from PracticePetstragram.web.views import HomeView, DashboardView

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('pet/add/', CreatePetView.as_view(), name='pet create'),
    path('pet/edit/', EditPetView.as_view(), name='pet edit'),
    path('pet/delete/', DeletePetView.as_view(), name='pet delete'),

    path('photo/details/<int:pk>/', PetPhotoDetailsView.as_view(), name='photo details'),
    path('photo/add/', PetPhotoCreateView.as_view(), name='photo create'),
    path('photo/like/<int:pk>/', like_pet_photo, name='like pet photo'),
    path('photo/edit/<int:pk>/', PetPhotoEditView.as_view(), name='photo edit'),
)