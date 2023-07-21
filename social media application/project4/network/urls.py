
from django.urls import path



from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('index', views.index, name='index'),
    path('create', views.create_post, name='create'),
    path('profile', views.profile, name='profile'),
    path('comments/<int:post_id>', views.comments, name='comments'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit'),
    path('following_page', views.following_page, name='following_page'),
    path('following_list', views.following_list, name='following_list'),  
    path('followers_list', views.followers_list, name='followers_list'), 
    path('other_profile_page/<int:user_id>', views.other_profile_page, name='other_profile_page'),

    #API's for js
    path('posts/<int:limit>/<int:start>', views.posts, name="posts"),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('like_post/<int:post_id>', views.like_post, name='like'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('follow/<int:post_id>', views.follow, name='follow'),
    path('following/<int:limit>/<int:start>', views.following, name="following"),
    path('other_profile/<int:user_id>', views.other_profile, name='other_profile'),

    #other 
    path('favicon.ico', views.favicon),
]
