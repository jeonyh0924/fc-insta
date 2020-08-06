from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from config.celery import create_users_send_mail_async

User = get_user_model()


@receiver(pre_save, sender=User)
def user_set_password(sender, instance, **kwargs):
    """
    user_set_password는 리시버 함수.
    User 모델은 sender에서 보낸 사람.
    pre_save는 시그널.
    User instance가 save 메서드 실행을 동작하기 전에 user_set_password가 수행 된다.
    """
    instance.set_password(instance.password)


@receiver(post_save, sender=User)
def create_user_send_to_mail(sender, created, instance, **kwargs):
    if created:
        create_users_send_mail_async.delay(instance.email)
