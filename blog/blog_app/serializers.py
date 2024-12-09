# blog_app/serializers.py
from rest_framework import serializers
from .models import Blog, Comment
from blog_app import models

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author_id', 'created_at', 'updated_at', 'likes', 'images']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'comment_text', 'author_id', 'created_at']
