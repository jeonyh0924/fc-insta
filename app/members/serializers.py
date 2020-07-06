from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import Relations, Profile

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

    def create(self, validated_data):
        context = validated_data.pop('context')
        username = context['request'].data.get('username')
        user = User.objects.create_user(**validated_data)

        """
        이러면 admin 페이지에서 유저 생성시 프로필이 생기지 않고 ->> 반례: admin페이지는 유저 안에 다른 속성을 넣지 못해서
         
        model save()에서 커스텀을 하려면 save에 어떤 인자를 보내야 받을 수 있을까?
        """
        pro = Profile.objects.create(
            user=user,
            username=username,
        )
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
