from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)  # ✅ Kullanıcı adı eklendi

    class Meta:
        model = BlogPost
        fields = ['id', 'user', 'title', 'content', 'image', 'created_at']
