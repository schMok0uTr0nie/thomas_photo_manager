# Generated by Django 4.1.4 on 2022-12-20 05:19

from django.db import migrations, models
import photon.models


class Migration(migrations.Migration):

    dependencies = [
        ('photon', '0013_alter_snapshot_category_alter_snapshot_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snapshot',
            name='photo',
            field=models.FileField(upload_to=photon.models.user_directory_path1, verbose_name='Фото'),
        ),
    ]