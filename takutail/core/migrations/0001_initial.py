# Generated by Django 5.1 on 2024-08-10 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Other',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('exclude', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('aroma', models.CharField(max_length=100)),
                ('sweetness', models.FloatField()),
                ('bitterness', models.FloatField()),
                ('sourness', models.FloatField()),
                ('alcohol_content', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Wari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('aroma', models.CharField(max_length=100)),
                ('sweetness', models.FloatField()),
                ('bitterness', models.FloatField()),
                ('sourness', models.FloatField()),
                ('exclude', models.BooleanField(default=False)),
            ],
        ),
    ]
