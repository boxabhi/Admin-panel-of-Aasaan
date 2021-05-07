# Generated by Django 3.1.3 on 2021-04-28 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0004_auto_20210323_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beneficiaries', models.CharField(max_length=100)),
                ('total', models.CharField(max_length=100)),
                ('total_males', models.CharField(max_length=100)),
                ('this_month_total', models.CharField(max_length=100)),
                ('males', models.CharField(max_length=100)),
                ('females', models.CharField(max_length=100)),
                ('this_fy_total', models.CharField(max_length=100)),
                ('this_fv_males', models.CharField(max_length=100)),
                ('this_fv_females', models.CharField(max_length=100)),
            ],
        ),
    ]
