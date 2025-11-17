from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Tüm alanlar zorunludur!'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Bu e-posta adresi zaten kayıtlı!'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username, email=email, password=make_password(password))
    user.save()

    # 🎯 Django Token Authentication için Token oluştur
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'message': 'Kayıt başarılı!',
        'token': str(token.key)  # 🔥 Artık sadece Django Token Authentication kullanılıyor
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])  # Yetkilendirme gerekmiyor, herkes giriş yapabilir
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Geçersiz e-posta veya şifre!'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        return Response({'error': 'Geçersiz e-posta veya şifre!'}, status=status.HTTP_400_BAD_REQUEST)

    # 🎯 Kullanıcıya Django Token Authentication token'ı döndür
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': str(token.key),  # 🔥 Kullanıcı artık JWT yerine Django Token alıyor
        'username': user.username
    }, status=status.HTTP_200_OK)
