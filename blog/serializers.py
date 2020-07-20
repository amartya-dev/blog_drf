from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from blog.models import User, Article, Comment, LikedArticle


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'email', 'password')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        exclude = ("likes", "slug", "publish")


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class LikedArticleSerializer(serializers.ModelSerializer):
    article = serializers.ReadOnlyField(source='article.title')

    class Meta:
        model = LikedArticle
        exclude = ("user",)


class LikeArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedArticle
        fields = ("article",)
