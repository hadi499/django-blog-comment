from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.blog_detail, name='detail'),
    path('post/delete/<int:pk>/', views.deletePost, name='delete_post'),
    path('post/update/<int:pk>/', views.updatePost, name='update_post'),
    path('create/', views.createPost, name='create'),
]
