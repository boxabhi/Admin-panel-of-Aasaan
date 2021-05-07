# Generated by Django 3.1.4 on 2021-04-16 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_scheduleinterview_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ClaimNo', models.CharField(blank=True, max_length=1000, null=True)),
                ('IFIG_NO', models.CharField(blank=True, max_length=1000, null=True)),
                ('Inward', models.CharField(blank=True, max_length=1000, null=True)),
                ('Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Month', models.CharField(blank=True, max_length=1000, null=True)),
                ('Employee_Code', models.CharField(blank=True, max_length=1000, null=True)),
                ('Inwarded_By', models.CharField(blank=True, max_length=1000, null=True)),
                ('Vendor_Code', models.CharField(blank=True, max_length=1000, null=True)),
                ('Vendor_Name', models.CharField(blank=True, max_length=1000, null=True)),
                ('Mail_Received_From', models.CharField(blank=True, max_length=1000, null=True)),
                ('Do_Name_PM_Name', models.CharField(blank=True, max_length=1000, null=True)),
                ('Claim_Type', models.CharField(blank=True, max_length=1000, null=True)),
                ('From_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('To_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Department', models.CharField(blank=True, max_length=1000, null=True)),
                ('PO_Number', models.CharField(blank=True, max_length=1000, null=True)),
                ('Invoice_No', models.CharField(blank=True, max_length=1000, null=True)),
                ('Invoice_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Invoice_Amount', models.CharField(blank=True, max_length=1000, null=True)),
                ('Ramco', models.CharField(blank=True, max_length=1000, null=True)),
                ('Document_No', models.CharField(blank=True, max_length=1000, null=True)),
                ('Entry_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Authorised_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Entry_Done_By', models.CharField(blank=True, max_length=1000, null=True)),
                ('USER_ID', models.CharField(blank=True, max_length=1000, null=True)),
                ('Payment', models.CharField(blank=True, max_length=1000, null=True)),
                ('Details', models.CharField(blank=True, max_length=1000, null=True)),
                ('Submision_date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Upload_Number', models.CharField(blank=True, max_length=1000, null=True)),
                ('UTR_NO', models.CharField(blank=True, max_length=1000, null=True)),
                ('Payment_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('UPLOAD_STATUS', models.CharField(blank=True, max_length=1000, null=True)),
                ('STATUS', models.CharField(blank=True, max_length=1000, null=True)),
                ('Remarks', models.CharField(blank=True, max_length=1000, null=True)),
                ('Received_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Objection', models.CharField(blank=True, max_length=1000, null=True)),
                ('Objection_Raised_By', models.CharField(blank=True, max_length=1000, null=True)),
                ('Query', models.CharField(blank=True, max_length=1000, null=True)),
                ('Mail_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Resolution_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Resolution_By', models.CharField(blank=True, max_length=1000, null=True)),
                ('Rejection_Date', models.CharField(blank=True, max_length=1000, null=True)),
                ('Rejection_Done_By', models.CharField(blank=True, max_length=1000, null=True)),
                ('Location', models.CharField(blank=True, max_length=1000, null=True)),
                ('Classification', models.CharField(blank=True, max_length=1000, null=True)),
                ('Reporting_Mngr', models.CharField(blank=True, max_length=1000, null=True)),
                ('Zonal_Head', models.CharField(blank=True, max_length=1000, null=True)),
                ('Zone', models.CharField(blank=True, max_length=1000, null=True)),
                ('Period', models.CharField(blank=True, max_length=1000, null=True)),
                ('Age', models.CharField(blank=True, max_length=1000, null=True)),
                ('HGS', models.CharField(blank=True, max_length=1000, null=True)),
                ('Remark', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
