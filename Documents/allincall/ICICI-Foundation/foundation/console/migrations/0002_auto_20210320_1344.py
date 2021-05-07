# Generated by Django 3.1.4 on 2021-03-20 08:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referral',
            name='datetime',
        ),
        migrations.AddField(
            model_name='otpverification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='otpverification',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='referral',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='referral',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
