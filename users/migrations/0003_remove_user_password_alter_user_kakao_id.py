# Generated by Django 4.0.3 on 2022-04-14 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_kakao_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AlterField(
            model_name='user',
            name='kakao_id',
            field=models.BigIntegerField(),
        ),
    ]