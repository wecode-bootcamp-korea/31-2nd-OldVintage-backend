# Generated by Django 4.0.3 on 2022-04-14 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Pairing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'pairings',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('grape', models.CharField(max_length=100)),
                ('bold', models.DecimalField(decimal_places=2, max_digits=3)),
                ('tannic', models.DecimalField(decimal_places=2, max_digits=3)),
                ('sweet', models.DecimalField(decimal_places=2, max_digits=3)),
                ('acidic', models.DecimalField(decimal_places=2, max_digits=3)),
                ('image_url', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'types',
            },
        ),
        migrations.CreateModel(
            name='Winery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('description', models.CharField(max_length=1000)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wineries', to='products.country')),
            ],
            options={
                'db_table': 'wineries',
            },
        ),
        migrations.CreateModel(
            name='ProductPairing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pairing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productpairings', to='products.pairing')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productpairings', to='products.product')),
            ],
            options={
                'db_table': 'productpairings',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='pairings',
            field=models.ManyToManyField(through='products.ProductPairing', to='products.pairing'),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.type'),
        ),
        migrations.AddField(
            model_name='product',
            name='winery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.winery'),
        ),
    ]
