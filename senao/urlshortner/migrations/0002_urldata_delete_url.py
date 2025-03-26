# Generated by Django 5.1.7 on 2025-03-25 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_url', models.URLField(max_length=2048, unique=True)),
                ('hash', models.CharField(max_length=10, unique=True)),
                ('expire_at', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Url',
        ),
    ]
