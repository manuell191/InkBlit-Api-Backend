# Generated by Django 4.1.7 on 2023-04-12 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_post_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='room',
            field=models.TextField(default='global', max_length=6),
        ),
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.TextField(max_length=6),
        ),
    ]
