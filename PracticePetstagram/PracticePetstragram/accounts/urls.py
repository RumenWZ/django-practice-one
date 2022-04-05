from django.urls import path

from PracticePetstragram.accounts.views import UserLoginView, UserLogoutView, UserRegisterView, ProfileDetailsView


urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('register/', UserRegisterView.as_view(), name='create user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),

    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
)