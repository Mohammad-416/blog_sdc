# blog_app/views.py
from rest_framework import generics, permissions
from .models import Blog, Comment, Image, Like
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from cloudinary.uploader import upload
from django.conf import settings
from blog_app.models import CustomUser
from rest_framework import status
from rest_framework.views import APIView

class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        # Validate image count
        images = request.FILES.getlist('images')
        if len(images) > 3:
            return Response({'error': 'Maximum 3 images allowed'}, status=400)

        # Create blog
        blog = Blog.objects.create(
            title=request.data.get('title'),
            content=request.data.get('content'),
            author_id=request.data.get('author_id')
        )

        # Upload images and associate with blog
        uploaded_images = []
        for image in images:
            try:
                # Upload to Cloudinary
                uploaded_image = upload(
                    image, 
                    folder='blog_images',  # Optional: organize uploads in a folder
                    overwrite=True,
                    resource_type='image'
                )
                
                # Create Image object
                image_obj = Image.objects.create(
                    image=uploaded_image['secure_url'],
                    blog = blog
                )
                
                # Add image to blog's images
                blog.images.add(image_obj)
                uploaded_images.append(image_obj)

            except Exception as e:
                # Handle upload errors
                blog.delete()  # Clean up the blog if image upload fails
                return Response({
                    'error': f'Image upload failed: {str(e)}', 
                    'detail': str(e)
                }, status=400)

        # Save blog to persist many-to-many relationship
        blog.save()

        # Serialize and return blog data
        serializer = self.serializer_class(blog)
        return Response(serializer.data)

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Get image URLs
        image_urls = [str(image.image.url) for image in instance.images.all()]
        
        # Add image URLs to the response data
        data = serializer.data.copy()
        data['images'] = image_urls
        
        return Response(data)


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
        
    # Validate author_id exists in request data
    if 'author_id' not in request.data:
        return Response({"error": "Author ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        author = CustomUser.objects.get(author_id=request.data['author_id'])
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid author ID"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user has already liked the post
    existing_like = Like.objects.filter(blog=blog, user=author).first()
    if existing_like:
        if existing_like.is_liked:
            blog.likes -= 1
            existing_like.is_liked = False
        else:
            blog.likes += 1
            existing_like.is_liked = True
    else:
        Like.objects.create(
            blog=blog,
            user=author,
            is_liked=True
        )
        blog.likes += 1

    blog.save()

    return Response({"likes": blog.likes})