# Generated by Django 4.0.3 on 2022-04-12 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_url',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]