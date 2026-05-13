from rest_framework import serializers
from .models import Post, Comment, Profile

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author_password_hash = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', 'comments', 'author_password_hash']

    def get_author_password_hash(self, obj):
        return "5f4dcc3b5aa765d61d8327deb882cf99"