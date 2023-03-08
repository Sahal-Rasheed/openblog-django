from django.urls import path
from .views import *

urlpatterns = [

    path('signup/', RegView.as_view(), name='register'),
    path('signin/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]