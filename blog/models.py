from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Color(models.TextChoices):
    RED = 'RED', _('Red')
    BLACK = 'BLACK', _('Black')
    WHITE = 'WHITE', _('White')
    GREN = 'GREEN', _('Green')
    YELLOW = 'YELLOW', _('Yellow')
    WINE = 'WINE', _('Wine')

class Category(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=20, choices=Color.choices, default=Color.WHITE)

    def __str__(self) -> str:
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)

    def publish(self) -> None:
        self.published_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        return self.title
    

