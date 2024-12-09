# blog_app/views.py
from rest_framework import generics, permissions
from .models import Blog, Comment, Image
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from cloudinary.uploader import upload
from django.conf import settings



class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        images = request.FILES.getlist('images')
        print(images)
        if len(images) > 3:
            return Response({'error': 'Maximum 3 images allowed'}, status=400)

        blog = Blog.objects.create(
            title=request.data.get('title'),
            content=request.data.get('content'),
            author_id=request.data.get('author_id')
        )
        print("In Upload")
        for image in images:
            uploaded_image = upload(image)
            print(uploaded_image['secure_url'])
            image_obj = Image(image=uploaded_image['secure_url'], blog=blog)
            image_obj.save()
            blog.image_url = uploaded_image['secure_url']
            print(blog.image)
            blog.save()
        print("out")

        serializer = self.serializer_class(blog)
        return Response(serializer.data)

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        author_id = request.data.get('author_id')
        if author_id and author_id == str(blog.author_id):
            serializer = self.serializer_class(data=request.data, instance=blog)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response({'error': 'You are not the author of this post'}, status=403)

    def destroy(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        author_id = request.data.get('author_id')
        if author_id and author_id == str(blog.author_id):
            blog.delete()
            return Response(status=204)
        return Response({'error': 'You are not the author of this post'}, status=403) 
    
    

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


