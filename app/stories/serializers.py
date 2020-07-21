from rest_framework import serializers

from members.serializers import UserSimpleSerializers
from stories.models import Story, StoryCheck


class StoryCheckSerializers(serializers.ModelSerializer):
    class Meta:
        model = StoryCheck
        fields = ('id', 'user', 'story')


class StorySerializers(serializers.ModelSerializer):
    check = StoryCheckSerializers(source='check_set', many=True, read_only=True)
    user = UserSimpleSerializers(read_only=True, )

    class Meta:
        model = Story
        fields = ('id', 'user', 'content', 'check', 'image', 'video')

    def create(self, validated_data):
        story = Story.objects.create(**validated_data)
        return story


class StoryRetrieveSerializers(serializers.ModelSerializer):
    check = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'user', 'content', 'image', 'check')

    def get_check(self, obj):
        ins, __ = StoryCheck.objects.get_or_create(
            user=self.context['request'].user,
            story=obj
        )
        serializer = StoryCheckSerializers(ins)
        return serializer.data
