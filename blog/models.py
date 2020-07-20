from django.db import models

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
    publish = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )
    top_image = models.ImageField(
        upload_to='articles/%Y/%m/%d'
    )
    likes = models.IntegerField()


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
