from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('novel', '小説'),
        ('business', 'ビジネス'),
        ('science', '科学'),
        ('history', '歴史'),
        ('comic', '漫画'),
        ('essay', 'エッセイ'),
        ('other', 'その他'),
    ]
    
    STATUS_CHOICES = [
        ('reading', '読書中'),
        ('interested', '興味がある'),
        ('finished', '読了'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=100)
    author = models.CharField("著者", max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    comment = models.TextField("コメント", max_length=200)
    rating = models.IntegerField("おすすめ度", choices=[(i, str(i)) for i in range(1, 6)])
    status = models.CharField("読書状況", max_length=20, choices=STATUS_CHOICES, default='reading')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title