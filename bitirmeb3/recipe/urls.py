from django.urls import path
from .views import RecipeListCreateView, RecipeDetailView, chatbot_cevap, chatbot_foto

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),  # Tarif listeleme ve oluşturma
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),  # Tarif detay
    path('create_recipe/', RecipeListCreateView.as_view(), name='create_recipe'),  # Tarif ekleme (POST)
    path('chatbot/', chatbot_cevap, name='chatbot'),
    path('chatbot-foto/', chatbot_foto),
]
