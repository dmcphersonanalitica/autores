from django.urls import path

from Login.views import *
#from core.administration.views.group.views import *


app_name = 'login'

urlpatterns = [
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('user/add/', UserCreateView.as_view(), name='user_add'),
    path('user/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('change/password/', UserChangePasswordView.as_view(), name='user_change_password'),
]