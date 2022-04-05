from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from PracticePetstragram.accounts.views import UserLoginView, UserLogoutView, UserRegisterView, ProfileDetailsView, \
    ChangePasswordView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('register/', UserRegisterView.as_view(), name='create user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),

    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit-password/', ChangePasswordView.as_view(), name='edit password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password change done'),
)