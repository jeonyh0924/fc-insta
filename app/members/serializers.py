from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import Relations

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}

        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RelationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Relations
        fields = ('id', 'from_user', 'to_user', 'related_type')
