from rest_framework.serializers import \
    (ModelSerializer,
     HyperlinkedIdentityField,
     SerializerMethodField,
     )

from ..models import Comment


class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
        ]

    def get_reply_count(self, comment):
        return comment.children().count() if comment.is_parent else 0


class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'replies',
            'timestamp',
        ]

    def get_replies(self, comment):
        if comment.is_parent:
            return ReplySerializer(comment.children(), many=True).data
        return None


class ReplySerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
        ]
