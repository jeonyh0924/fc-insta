from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from members.models import Relations, Profile
from posts.models import Post

# from posts.serializers import PostUpdateSerializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        context = validated_data.pop('context')
        username = context['request'].data.get('username')

        user = User.objects.create_user(**validated_data)
        user.profile.username = username
        user.profile.save()

        return user


class ProfileSerializers(serializers.ModelSerializer):
    relation = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_relation(self, obj):
        relation = Relations.objects.get(from_user=self.context.request.user, to_user=obj.user_id)
        related_type = relation.related_type
        data = {
            "relation_id": relation.id,
            "related_type": related_type
        }
        return data


class UserSerializers(serializers.ModelSerializer):
    profile = ProfileSerializers()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'profile',)
        extra_kwargs = {
            'password': {'write_only': True}

        }


class FollowerUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class RelationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Relations
        fields = ('id', 'from_user', 'to_user', 'related_type')

    def create(self, validated_data):
        from_user = validated_data['from_user']
        to_user = validated_data['to_user']
        if from_user == to_user:
            raise ValidationError(f'Unable create to same user')
        return super().create(validated_data)


class UserSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class ProfileDetailSerializers(serializers.ModelSerializer):
    user = UserSimpleSerializers()
    profile_post_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'username', 'introduce', 'follower_count', 'following_count', 'profile_post_count',
                  )

    def get_profile_post_count(self, obj):
        count = Post.objects.filter(user=obj.user).count()
        return count


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'introduce'
        )


class ChangePassSerializers(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True, )
    new_password = serializers.CharField(max_length=128, required=True, )

    def update(self, instance, validated_data):
        old_password = validated_data.get('old_password')
        new_password = validated_data.get('new_password')
        if instance.check_password(old_password):
            instance.set_password(new_password)
            # instance.save 하면 모델의 create가 된다.
            return instance
        raise exceptions.AuthenticationFailed()
