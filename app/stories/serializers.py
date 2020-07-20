from rest_framework import serializers

from members.serializers import UserSimpleSerializers
from stories.models import Story, StoryImage, StoryCheck


class StoryCheckSerializers(serializers.ModelSerializer):
    class Meta:
        model = StoryCheck
        fields = ('id', 'user', 'story')


class StoryImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = StoryImage
        fields = ('image',)


class StorySerializers(serializers.ModelSerializer):
    image = StoryImageSerializers(many=True, read_only=True, )
    check = StoryCheckSerializers(source='check_set', many=True,)
    user = UserSimpleSerializers()

    class Meta:
        model = Story
        fields = ('id', 'user', 'content', 'image', 'check')

    def create(self, validated_data):
        story = Story.objects.create(**validated_data)
        images = self.context['request'].FILES
        image_list = []
        for i in images.getlist('image'):
            image_list.append(StoryImage(story=story, image=i))
        StoryImage.objects.bulk_create(image_list)
        return story


class StoryRetrieveSerializers(serializers.ModelSerializer):
    image = StoryImageSerializers(many=True, read_only=True, )
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
