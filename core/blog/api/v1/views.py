from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter ,OrderingFilter
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,IsAuthenticatedOrReadOnly,)
from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import PostSerializer, CategorySerializer,PostCommentSerializer
from .paginations import CustomPagination
from .permissions import IsOwnerOrReadOnly
# from .filter import PostFilter
from ...models import Post,Category,PostComment


# 4.2 viewsets.ModelViewSet (Router Structure)

class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_classes = PostFilter
    filterset_fields = ['author','category','status']
    search_fields = ['title','content']
    ordering_fields = ['published_date','counted_views']
    pagination_class = CustomPagination
    
    @action(detail=False, methods=['get'])
    def latest_posts(self, request):
        latest_posts = self.queryset.order_by('-published_date')[:2]
        serializer = self.serializer_class(latest_posts, many=True, context={'request':request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def latest_post(self, request, pk=None):
        latest_post = self.queryset.order_by('-published_date')[:2]
        serializer = self.serializer_class(latest_post, many=True, context={'request': request})
        return Response(serializer.data)
    
    """
    @action(detail=True, methods=['get'])
    def latest_post(self, request, pk=None):
        try:
            latest_post = self.get_object()  # Get the specific post by pk
            serializer = self.serializer_class(latest_post, context={'request': request})
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=404)
    """
    
    @action(detail=True, methods=['get'])
    def latest_posts(self, request, pk=None):
        most_views = self.queryset.order_by('-counted_views')[:2]
        serializer = self.serializer_class(most_views, many=True, context={'request':request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def posts_author(self, request, pk=None):
        posts_author = self.queryset.filter(author=pk)
        serializer = self.serializer_class(posts_author, many=True, context={'request':request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def posts_category(self, request, pk=None):
        posts_category = self.queryset.filter(category=pk)
        serializer = self.serializer_class(posts_category, many=True, context={'request':request})
        return Response(serializer.data)
    
    """
    @action(detail=True, methods=['get'])
    def posts_topic(self, request, pk=None):
        posts_topic = self.queryset.filter(topic=pk)
        serializer = self.serializer_class(posts_topic, many=True, context={'request':request})
        return Response(serializer.data)
    """


"""
from django.shortcuts import render

def posts_list(request):
    return render(request, 'blog/posts.html')
"""

   
class PostCommentModelViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]    
    
    
    # def get_queryset(self):
    #     return self.queryset.filter(author=self.request.user)
    
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
    
    # def get_permissions(self):
    #     if self.action == 'create':
    #         permission_classes = [IsAuthenticated]
    #     elif self.action in ['update','partial_update','destroy']:
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAuthenticatedOrReadOnly]
    #     return [permission() for permission in permission_classes]
    
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return PostSerializer
    #     elif self.action == 'retrieve':
    #         return PostSerializer
    #     return PostSerializer


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()