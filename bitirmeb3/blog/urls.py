from django.urls import path
from .views import BlogListCreateView, BlogDetailView, BlogUpdateDeleteView

urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogUpdateDeleteView.as_view(), name='blog-update-delete'),
    path('blogs/<int:pk>/detail/', BlogDetailView.as_view(), name='blog-detail'),  # 👈 Bu eklendi
]
