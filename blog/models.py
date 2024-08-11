from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

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

    class Meta:
        verbose_name_plural = "Categories"

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
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
    
    class HomePage(Page):
        intro = RichTextField(blank=True)

        content_panels = Page.content_panels + [
            FieldPanel('intro')
        ]

    class BlogPage(Page):
        author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        date = models.DateField("Post date")
        intro = models.CharField(max_length=200)
        text = RichTextField(blank=True)

        search_fields = Page.search_fields + [
            index.SearchField('intro'),
            index.SearchField('text'),
        ]

        content_panels = Page.content_panels + [
            FieldPanel('author'),
            FieldPanel('date'),
            FieldPanel('intro'),
            FieldPanel('text'),
        ]