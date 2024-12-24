# blog_app/urls.py
from django.urls import path
from .views import BlogListCreateView, BlogDetailView, LikePostView, add_comment

urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/comments/', add_comment, name='add-comment'),
    path('blogs/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
]
