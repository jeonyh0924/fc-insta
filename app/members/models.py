from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.core.cache import cache

# User = get_user_model()
from django.db.models import F
from rest_framework.generics import get_object_or_404


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

            user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    relations_users = models.ManyToManyField(
        'self',
        related_name='+',
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            email, domain = self.email.split('@')
            Profile.objects.create(
                user=self,
                username=email
            )
        else:
            cache.delete(f'user{self.pk}')
            super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def delete(self, **kwargs):
        cache.delete(f'user{self.pk}')
        return super().delete()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def follow(self):
        # 내가 팔로우를 건 유저
        user = User.objects.filter(
            to_users_relation__from_user=self,
            to_users_relation__related_type='f'
        ).select_related('profile')
        return user

    @property
    def follower(self):
        # 나를 팔로우를 건 유저
        user = User.objects.filter(
            from_users_relation__to_user=self,
            from_users_relation__related_type='f'
        ).select_related('profile')
        return user

    @property
    def blocker(self):
        # 나를 블락을 건 유저
        user = User.objects.filter(
            from_users_relation__to_user=self,
            from_users_relation__related_type='b'
        )
        return user

    @property
    def block(self):
        # 내가 블락을 건 유저
        user = User.objects.filter(
            to_users_relation__from_user=self,
            to_users_relation__related_type='b'
        ).select_related('profile')
        return user


class Relations(models.Model):
    CHOICE_RELATIONS_TYPE = (
        ('f', 'follow'),
        ('b', 'block'),
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        related_query_name='from_users_relation',
        null=True,
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_users_relation',
        null=True,
    )
    related_type = models.CharField(
        choices=CHOICE_RELATIONS_TYPE,
        max_length=10,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
            릴레이션이 생성이 될 때, F면 +1 B은 영향을 주지 않는다.
                    삭제가 될 때 F면 -1 B은 영향을 주지 않는다.
            """
        from_user = get_object_or_404(User, pk=self.from_user_id)
        to_user = get_object_or_404(User, pk=self.to_user_id)

        created = self.pk is None

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

        """
         - 새로 생성하는 유저가 'f' -> from_user following count += 1, to_user follower count += 1
         - Block Relation -> Follow Relation 으로 update 
         인스타그램은 기존에 팔로우 -> 블락은 같은 인스턴스
         블락-> 팔로우는 블락이 걸린 릴레이션 자체를 삭제 후 새로 팔로우에 대한 릴레이션을 요청해야 한다. 
        """

        if created and self.related_type == 'f':
            # 팔로우를 건 유저의 팔로윙 카운트 증가.
            from_user.profile.following_count = F('following_count') + 1
            to_user.profile.follower_count = F('follower_count') + 1
            from_user.profile.save()
            to_user.profile.save()

        if created is False and self.related_type == 'b':
            from_user.profile.following_count = F('following_count') - 1
            to_user.profile.follower_count = F('follower_count') - 1
            from_user.profile.save()
            to_user.profile.save()

    def delete(self, using=None, keep_parents=False):
        from_user = get_object_or_404(User, pk=self.from_user_id)
        to_user = get_object_or_404(User, pk=self.to_user_id)

        if self.related_type == 'f':
            # 팔로우를 건 유저의 팔로윙 카운트 증가.
            from_user.profile.following_count = F('following_count') - 1
            to_user.profile.follower_count = F('follower_count') - 1
            from_user.profile.save()
            to_user.profile.save()
        return super().delete(using=None, keep_parents=False)


class Profile(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
    )
    username = models.CharField(
        max_length=15,
    )
    introduce = models.CharField(
        max_length=100,
        null=True,
    )
    # 나를 팔로우 하고 있는 사람의 수
    follower_count = models.IntegerField(default=0)
    # 내가 팔로우를 하고 있는 사람의 수
    following_count = models.IntegerField(default=0)


class RecentlyUser(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user',
        related_query_name='recently_from_user',
        null=True,
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user',
        related_query_name='recently_to_user',
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, **kwargs):
        user_query = User.objects.filter(recently_to_user__from_user=1)
        print(User.objects.filter(recently_to_user__from_user=self.from_user.id))
        if len(user_query) >= 2:
            user_query[0].delete()
            print(User.objects.filter(recently_to_user__from_user=self.from_user.id))
        try:
            ins = RecentlyUser.objects.get(from_user=self.from_user, to_user=self.to_user)
            ins.delete()
            print(User.objects.filter(recently_to_user__from_user=self.from_user.id))
            return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        except RecentlyUser.DoesNotExist:
            print(User.objects.filter(recently_to_user__from_user=self.from_user.id))
            return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
