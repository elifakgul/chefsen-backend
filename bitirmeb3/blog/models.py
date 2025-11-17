from django.conf import settings
from django.db import models

class BlogPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)  # 📌 Yeni eklenen görsel alanı
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
