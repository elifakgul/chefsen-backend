from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    search_fields = ('title', 'user__username')
    list_filter = ('category', 'created_at')
