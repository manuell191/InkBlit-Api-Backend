# Generated by Django 4.1.1 on 2023-01-24 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='admin',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='api.profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='members',
            field=models.ManyToManyField(related_name='joinedRoom', to='api.profile'),
        ),
    ]