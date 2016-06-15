from rest_framework.serializers import \
    (ModelSerializer,
     HyperlinkedIdentityField,
     SerializerMethodField,
     )

from comments.api.serializers import CommentSerializer
from comments.models import Comment

from ..models import Post

post_detail_url = HyperlinkedIdentityField(
    view_name='posts-api:detail',
    lookup_field='pk',
)


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
            'read_time',
        ]


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'slug',
            'content',
            'publish',
        ]

    def get_user(self, post):
        return post.user.username


class PostDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()
    markdown = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'user',
            'title',
            'content',
            'image',
            'publish',
            'updated',
            'read_time',
            'markdown',
            'comments',
        ]

    def get_user(self, post):
        return post.user.username

    def get_markdown(self, post):
        return post.markdown

    def get_image(self, post):
        try:
            image = post.image.url
        except ValueError:
            image = None
        return image

    def get_comments(self, post):
        comment_qs = Comment.objects.filter_by_instance(post)
        comments = CommentSerializer(comment_qs, many=True).data
        return comments
