from django.urls import path
from .views import *

urlpatterns = [

    path('userprofile/', NUserProfile.as_view(), name='user_profile'),
    path('userprofile_add/', AddProfile.as_view(), name='add_user_profile'),
    path('userprofile_update/<int:id>', UpdateProfile.as_view(), name='update_user_profile'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('my_blogs/', MyBlogs.as_view(), name='my_blogs'),
    path('update_blog/<int:pk>', UpdateBlog.as_view(), name='update_blog'),
    path('delete_blog/<int:pk>', DeleteBlog.as_view(), name='delete_blog'),
    path('add_comment/<int:bid>', AddComments, name='comment'),
    path('add_like/<int:id>', AddLike, name='addlike'),
    path('remove_like/<int:id>', RemoveLike, name='removelike'),
    path('follow/<int:id>', Follow, name='follow'),

]