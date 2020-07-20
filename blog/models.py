from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from django.contrib.auth.models import User


class Article(models.Model):
    STATUS_CHOICES = (
        ("Draft", "draft"),
        ("Published", "published")
    )

    title = models.CharField(
        max_length=250
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    slug = models.SlugField(
        max_length=250
    )
    publish = models.DateTimeField(
        default=timezone.now
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft"
    )
    top_image = models.ImageField(
        upload_to='articles/%Y/%m/%d'
    )
    body = models.TextField()
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(
        max_length=100
    )
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return self.article.title


class LikedArticle(models.Model):
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
