from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Giriş yapmayanlar sadece görebilir
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']  # veya modelde hangi alanlar varsa


    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Tarif eklemek için giriş yapmalısınız!")  
        serializer.save(user=self.request.user)

# Tarif detayları görüntüleme, güncelleme ve silme view'ı
class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  

    def get_object(self):
        recipe = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:  # Eğer güncelleme ya da silme yapılıyorsa
            if recipe.user != self.request.user:  # Eğer tarifin sahibi değilse izin verme
                raise PermissionDenied("Bu tarifi güncelleme veya silme yetkiniz yok!")
        return recipe
    
@csrf_exempt
def chatbot_cevap(request):
    if request.method == "POST":
        soru = request.POST.get("soru", "")
        try:
            response = requests.post("http://127.0.0.1:8001/api/soru", data={"soru": soru})
            return JsonResponse(response.json())
        except Exception as e:
            return JsonResponse({"error": "Chatbot sistemine ulaşılamadı", "detay": str(e)}, status=500)
    
    elif request.method == "GET":
        return JsonResponse({
            "bilgi": "Lütfen POST isteği ile 'soru' parametresi gönderin. Örnek: {'soru': 'patates ile ne yapılır?'}"
        })

    return JsonResponse({"error": "Yalnızca GET ve POST destekleniyor."}, status=405)


@csrf_exempt
def chatbot_foto(request):
    if request.method == "POST":
        foto = request.FILES.get("foto")
        if not foto:
            return JsonResponse({"error": "Fotoğraf dosyası eksik"}, status=400)

        try:
            files = {"file": (foto.name, foto.read(), foto.content_type)}
            response = requests.post("http://127.0.0.1:8001/api/foto", files=files)
            return JsonResponse(response.json())
        except Exception as e:
            return JsonResponse({"error": "Görsel işleme sırasında hata oluştu", "detay": str(e)}, status=500)
    
    elif request.method == "GET":
        return JsonResponse({
            "bilgi": "Lütfen POST ile bir görsel yükleyin. Form field: 'foto'"
        })

    return JsonResponse({"error": "Yalnızca GET ve POST destekleniyor."}, status=405)