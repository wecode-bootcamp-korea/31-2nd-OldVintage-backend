# Generated by Django 4.0.3 on 2022-04-13 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_pairing_image_url_product_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairing',
            name='image_url',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.CharField(max_length=1000),
        ),
    ]