from rest_framework import generics, permissions
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class BlogListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # ✅ Giriş yapmadan görüntüleyebilir, ancak ekleyemez
    parser_classes = (MultiPartParser, FormParser)  # 📌 Görsel yükleme için destek

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Blog sahibini kaydet

class BlogDetailView(generics.RetrieveAPIView):  
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]  # ✅ Blog detayını herkes görebilir

class BlogUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]  # ✅ Güncelleme/Silme için giriş zorunlu
    parser_classes = (MultiPartParser, FormParser)  # 📌 Görsel yükleme için destek

    def perform_update(self, serializer):
        blog = self.get_object()
        if self.request.user.username != blog.user.username:  # ✅ Kullanıcı adı ile kontrol
            raise permissions.PermissionDenied("Bu blogu güncelleme yetkiniz yok!")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.username != instance.user.username:  # ✅ Kullanıcı adı ile kontrol
            raise permissions.PermissionDenied("Bu blogu silme yetkiniz yok!")
        instance.delete()
