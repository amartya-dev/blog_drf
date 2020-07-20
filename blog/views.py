from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from blog.models import Article, Comment, LikedArticle
from blog.serializers import UserSerializer, ArticleSerializer, \
    CommentSerializer, LikedArticleSerializer, LikeArticleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikedArticleListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikedArticleSerializer

    def get_queryset(self):
        return LikedArticle.objects.filter(user=self.request.user)


class LikeArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serialized_data = LikeArticleSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=ValueError):
            article = get_object_or_404(Article, pk=int(serialized_data["article"].value))
            article.likes += 1
            LikedArticle.objects.create(
                article=article,
                user=self.request.user
            )
            article.save()
            return Response(
                {"message": "Liked the article"},
                status=status.HTTP_200_OK
            )
