# Generated by Django 4.0.3 on 2022-04-16 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_grape'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='grape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.grape'),
        ),
    ]
