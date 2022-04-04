from django.urls import path

from PracticePetstragram.accounts.views import UserLoginView, UserLogoutView, UserRegisterView
from PracticePetstragram.web.views import CreateProfileView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('register/', UserRegisterView.as_view(), name='create user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
)