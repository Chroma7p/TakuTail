# Generated by Django 5.1 on 2024-08-11 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='alcohol_content',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
