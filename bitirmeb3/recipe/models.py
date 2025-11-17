from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Kahvaltı'),
        ('lunch', 'Ana Yemek'),
        ('soup', 'Corba'),
        ('dessert', 'Tatlı'),
        ('salad', 'Salata'),
        ('other', 'Diğer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Kullanıcı ile bağlantı
    title = models.CharField(max_length=255)  # Tarif başlığı
    ingredients = models.TextField()  # Tarif malzemeleri
    instructions = models.TextField()  # Tarif yapılışı
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # Tarif kategorisi
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)  # Tarif görseli
    created_at = models.DateTimeField(auto_now_add=True)  # Otomatik tarih ekleme

    def __str__(self):
        return self.title

