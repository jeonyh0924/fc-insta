from rest_framework import serializers

from stories.models import Story, StoryImage


class StoryImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = StoryImage
        field = ('image',)


class StorySerializers(serializers.ModelSerializer):
    image = StoryImageSerializers(many=True, read_only=True,)

    class Meta:
        model = Story
        fields = ('id', 'user','content', 'image')
        # read_only_fields = ['image', ]

    def create(self, validated_data):
        return super().create(validated_data)
