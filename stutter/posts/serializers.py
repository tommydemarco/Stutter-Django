from rest_framework import serializers 
from .models import Post

#model serializer for actions on a post
class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in ['like', 'unlike', 'repost']:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value

#model serializer for posts
class PostCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'likes']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        if len(value) > 300:
            raise serializers.ValidationError("This tweet is too long")
        return value



class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = PostCreateSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'content', 'likes', 'is_retweet', 'parent']

    def get_likes(self, obj):
        return obj.likes.count()

    # def get_content(self, obj):
    #     content = obj.content
    #     if obj.is_retweet:
    #         content = obj.parent.content 
    #     return content