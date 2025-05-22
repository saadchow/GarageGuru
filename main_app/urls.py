from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('messages/', views.messages, name='messages'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),
    # path('posts/create/', views.PostCreate.as_view(), name='posts_create'),
    path('posts/create/', views.posts_create, name='posts_create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
    path('posts/<int:post_id>/delete_photo/<int:photo_id>', views.delete_photo, name='delete_photo'),
    path('posts/<int:post_id>/add_comment/<int:user_id>', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/commentDelete/<int:comment_id>', views.delete_comment, name='comment_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('posts/<int:post_id>/add_like/<int:user_id>', views.add_like, name='add_like'),
    path('posts/<int:post_id>/add_like_detail/<int:user_id>',views.add_like_detail, name='add_like_detail'),
    path('posts/<int:post_id>/likes', views.likes_detail, name='likes_detail'),
    path('profile/<int:user_id>/username', views.username_update, name='username_update'),
    path('profile/<int:user_id>/username/success', views.username_updated, name='username_updated'),
    path('profile/<int:user_id>/bio', views.bio_update, name='bio_update'),
    path('profile/<int:user_id>/bio/success', views.bio_updated, name='bio_updated'),
    path('profile/<int:user_id>/photo', views.user_photo_update, name='user_photo_update'),
    path('posts/<int:post_id>/likes', views.likes_detail, name='likes_detail'),
    path('send_message/', views.send_message, name='send_message'),   
    path('search/<str:hashtag>/', views.search_by_hashtag, name='search_by_hashtag'),
]
