from rest_framework import serializers 
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    '''serializer for the API'''

    class Meta:
        model = Post
        fields = ['content']
    
    def validate_content(self, value):
        if len(value) > 300:
            raise serializers.ValidationError('This post is too long')
        return value 