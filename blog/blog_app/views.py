# blog_app/views.py
from rest_framework import generics, permissions
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@api_view(['POST'])
def add_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(blog=blog, author=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def like_post(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.likes += 1
    blog.save()
    return Response({"likes": blog.likes})
