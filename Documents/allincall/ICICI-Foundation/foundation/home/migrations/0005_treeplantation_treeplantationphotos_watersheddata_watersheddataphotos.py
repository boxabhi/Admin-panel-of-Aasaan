# Generated by Django 3.1.4 on 2021-04-15 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_scheduleinterview'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreePlantation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_plantation', models.DateField()),
                ('isa_location', models.CharField(max_length=100)),
                ('no_of_trees', models.IntegerField()),
                ('varieties', models.IntegerField()),
                ('occasion', models.CharField(max_length=100)),
                ('parternship', models.CharField(max_length=1000)),
                ('staff', models.CharField(max_length=1000)),
                ('post_plantation_care_by', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='WatershedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name_of_school', models.CharField(max_length=1000)),
                ('name_of_village', models.CharField(max_length=1000)),
                ('block', models.CharField(max_length=1000)),
                ('district', models.CharField(max_length=1000)),
                ('terrace', models.CharField(max_length=1000)),
                ('reservoir_type', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='WatershedDataPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='water')),
                ('water_shed_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.watersheddata')),
            ],
        ),
        migrations.CreateModel(
            name='TreePlantationPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='trees')),
                ('tree_plantation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.treeplantation')),
            ],
        ),
    ]
