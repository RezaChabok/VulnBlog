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

    #SQL Injection
    # New (Secure)
    def get_queryset(self):
        queryset = Post.objects.all()
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset


# New (Secure)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, user_id):
    if request.user.id != user_id:
        return Response({'error': 'Access denied'}, status=403)
    user = User.objects.get(id=user_id)
    return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': "5f4dcc3b5aa765d61d8327deb882cf99"
        })