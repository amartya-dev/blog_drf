from django.urls import include, path
from rest_framework import routers
from blog.views import UserViewSet, ArticleViewSet, CommentViewSet, LikedArticleListView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'article', ArticleViewSet)
router.register(r'comment', CommentViewSet)

app_name = 'blog'
urlpatterns = [
    path('', include(router.urls)),
    path('liked/', LikedArticleListView.as_view(), name="liked_articles")
]
