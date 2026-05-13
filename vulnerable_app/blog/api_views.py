from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth.models import User
import json

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Post.objects.all()
        q = self.request.query_params.get('q', None)
        if q:
            queryset = Post.objects.raw(f"SELECT * FROM blog_post WHERE title LIKE '%{q}%'")
        return queryset

@api_view(['GET'])
def user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': "5f4dcc3b5aa765d61d8327deb882cf99"
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)