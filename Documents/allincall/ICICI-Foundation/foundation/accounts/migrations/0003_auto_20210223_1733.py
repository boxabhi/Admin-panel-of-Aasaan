# Generated by Django 3.1.4 on 2021-02-23 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210222_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]