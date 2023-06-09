from django.urls import path
from mwk.modules.main.views.comment_view_set import CommentViewSet
from mwk.modules.main.views.post_view_set import PostViewSet

urlpatterns = [
    path("", PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='feed'),
    path("<int:pk>/", PostViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'}), name='post'),
    path("<int:pk>/comments/", PostViewSet.as_view({'get': 'get_all_comments'}), name='post_comments'),
    path("like/", PostViewSet.as_view({'put': 'like_post'}), name='like'),
    path("categories/", PostViewSet.as_view({'get': 'get_categories'}), name='post_categories'),

    path("comments/", CommentViewSet.as_view({'post': 'create'})),
    path("comment/<int:pk>/", CommentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'})),
    path("comment/<int:pk>/descendants/", CommentViewSet.as_view({'get': 'get_comment_replies'})),
    path("comment/like/", CommentViewSet.as_view({'put': 'like_post_comment'}), name='like_post_comment'),
]
