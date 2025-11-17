from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)  # 🔥 Kullanıcı ID yerine kullanıcı adı dönüyor

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'ingredients', 'instructions', 'category', 'image', 'created_at']
        read_only_fields = ['user', 'created_at']

