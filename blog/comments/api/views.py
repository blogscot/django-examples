from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView)

from rest_framework.permissions import \
    (AllowAny,
     IsAuthenticated,
     IsAdminUser,
     IsAuthenticatedOrReadOnly,
     )

from posts.api.pagination import \
    (PostLimitOffsetPagination,
     PostPageNumberPagination)

from posts.api.permissions import IsOwnerOrReadOnly

from ..models import Comment
from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        slug = self.request.GET.get('slug')
        parent_id = self.request.GET.get('parent_id', None)

        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user,
        )


class CommentRetrieveAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


# class PostUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly,
#                           IsAdminUser,
#                           IsOwnerOrReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name', 'user__last_name']
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        posts = Comment.objects.all()
        query = self.request.GET.get('q')
        if query:
            posts = posts.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return posts


# class PostDestroyAPIView(DestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated,
#                           IsAdminUser,
#                           IsOwnerOrReadOnly]
