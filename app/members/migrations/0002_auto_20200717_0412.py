# Generated by Django 3.0.7 on 2020-07-17 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relations',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_user_relations', related_query_name='from_users_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='relations',
            name='to_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user_relations', related_query_name='to_users_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='relations',
            unique_together={('from_user', 'to_user')},
        ),
    ]
