from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet, user_profile
from .views import post_detail, edit_post

router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:user_id>/profile/', user_profile, name='user-profile'),
    path('post/<int:post_id>/', post_detail, name='post-detail'),
    path('post/<int:post_id>/edit/', edit_post, name='edit-post'),
]