# blog_app/serializers.py
from rest_framework import serializers
from .models import Blog, Comment, Image
from blog_app import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'comment_text', 'author_id', 'created_at']


class BlogSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author_id', 'created_at', 'updated_at', 'likes', 'images', 'comment']
