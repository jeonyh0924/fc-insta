from cacheops import cached
from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from members.models import Relations, Profile, RecentlyUser
from posts.models import Post

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return super().create(validated_data)

    def save(self, **kwargs):
        return super().save(**kwargs)


class ProfileSerializers(serializers.ModelSerializer):
    relation = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'username', 'introduce', 'follower_count', 'following_count', 'relation',)

    def get_relation(self, obj):
        try:
            relation = Relations.objects.get(from_user=self.context.user, to_user=obj.user_id)
            related_type = relation.related_type
            data = {
                "relation_id": relation.id,
                "related_type": related_type
            }
            return data
        except Relations.DoesNotExist:
            if obj.user_id == self.context.user.id:
                data = {
                    "relation": "self"
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

    @property
    def data(self):
        return super().data()


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


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'introduce'
        )


class UserSimpleSerializers(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'profile')


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


class UserProfileSerializers(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'profile')


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


class RecentlyUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = RecentlyUser
        fields = ('id', 'from_user', 'to_user')

    def create(self, validated_data):
        return super().create(validated_data)
