# Generated by Django 4.0.3 on 2022-04-13 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='kakao_id',
            field=models.IntegerField(null=True),
        ),
    ]
