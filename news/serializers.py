from rest_framework import serializers
from taggit.serializers import TagListSerializerField
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'tags', 'source', 'created_at']
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        instance = News.objects.create(**validated_data)

        if tags:
            instance.tags.add(*tags)
        return instance


