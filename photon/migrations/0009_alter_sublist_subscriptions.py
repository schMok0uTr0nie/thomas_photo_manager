# Generated by Django 4.1.4 on 2022-12-18 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photon', '0008_alter_snapshot_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sublist',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, related_name='subscriptions', to='photon.profile'),
        ),
    ]