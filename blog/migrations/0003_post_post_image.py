# Generated by Django 4.1.7 on 2023-05-08 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]