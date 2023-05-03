from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mwk.modules.main.views.comment_view_set import CommentViewSet
from mwk.modules.main.views.post_view_set import PostViewSet

router = DefaultRouter()

router.register(r'', PostViewSet, basename='feed')
router.register(r'<int:pk>/', PostViewSet, basename='post')
router.register(r'<int:pk>/comments/', PostViewSet, basename='post_comments')
router.register(r'like/', PostViewSet, basename='like')
router.register(r'categories/', PostViewSet, basename='post_categories')

router.register(r'comments', CommentViewSet)
router.register(r'comment/<int:pk>/', CommentViewSet, basename='comment')
router.register(r'comment/<int:pk>/descendants/', CommentViewSet, basename='comment_descendants')
router.register(r'comment/like/', CommentViewSet, basename='like_comment')

urlpatterns = [
    path('', include(router.urls)),
]
