from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models


# User = get_user_model()

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
        through='Relations',
        # relations_users에 대한 역방향 참조에 대해서 거부한다.
        related_name='+',
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

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
        )
        return user

    @property
    def follower(self):
        # 나를 팔로우를 건 유저
        user = User.objects.filter(
            from_users_relation__to_user=self,
            from_users_relation__related_type='f'
        )
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
        )
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
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_users_relation',
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
            ('to_user', 'from_user'),
        )


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
