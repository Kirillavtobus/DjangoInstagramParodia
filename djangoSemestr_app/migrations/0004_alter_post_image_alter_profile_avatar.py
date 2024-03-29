# Generated by Django 4.2.9 on 2024-01-27 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoSemestr_app', '0003_alter_post_image_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='djangoSemestr/media/profile_photo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(upload_to='djangoSemestr/media/project_photo'),
        ),
    ]
