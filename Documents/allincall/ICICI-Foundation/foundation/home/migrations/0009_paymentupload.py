# Generated by Django 3.1.4 on 2021-04-16 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_paymentsheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.TextField()),
                ('is_uploaded', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
