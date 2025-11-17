from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneli
    # Kullanıcı işlemleri
    path('api/user/', include('user.urls')),
    # Tarif işlemleri
    path('api/', include('recipe.urls')),
    path('api/', include('blog.urls')),
    # Token Authentication (Django Token Auth için)
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    # JWT Authentication (Django Simple JWT için)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
