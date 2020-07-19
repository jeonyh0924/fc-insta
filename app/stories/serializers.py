from rest_framework import serializers

from stories.models import Story, StoryImage


class StoryImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = StoryImage
        fields = ('image',)


class StorySerializers(serializers.ModelSerializer):
    image = StoryImageSerializers(many=True, read_only=True, )

    class Meta:
        model = Story
        fields = ('id', 'user', 'content', 'image')

    def create(self, validated_data):
        story = Story.objects.create(**validated_data)
        images = self.context['request'].FILES
        image_list =[]
        for i in images.getlist('image'):
            image_list.append(StoryImage(story=story, image=i))
        StoryImage.objects.bulk_create(image_list)
        return story
