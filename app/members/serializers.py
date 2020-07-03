from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import Relations

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save(username=self.context['request'].data.get('username'))
        return user


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}

        }


class RelationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Relations
        fields = ('id', 'from_user', 'to_user', 'related_type')
