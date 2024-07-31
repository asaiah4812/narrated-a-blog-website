from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Article.Status.PUBLISHED)
    
class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Article.Status.DRAFT)

class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=250)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    image = models.ImageField(upload_to='article_images/')
    tags = models.ManyToManyField('Tag')
    publish = models.DateTimeField(default=timezone.now)
    love = models.ManyToManyField(User, related_name='love_articles', through="LovedArticle")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()
    
    class Meta:
        ordering = ['-publish']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        indexes = [
            models.Index(fields=['-publish']),
            ]
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug, self.id])
    
class LovedArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"liked by {self.user.username}"

    
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)

    
    def __str__(self):
        return self.name
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')
    dislikes = models.ManyToManyField(User, related_name="dislikedcomments", through="DisLikedComment")
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        try:
            return str(self.author.username)
        except:
            return str('No author')
        
    class Meta:
        ordering = ['-created']


class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"liked by {self.user.username}"
    
class DisLikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"liked by {self.user.username}"



