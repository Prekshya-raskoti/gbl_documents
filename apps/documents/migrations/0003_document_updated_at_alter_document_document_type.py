# Generated by Django 5.1.7 on 2025-04-07 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.CharField(choices=[('citizenship', 'Citizenship'), ('Citizenship Back', 'Citizenship Back'), ('bank_details', 'Bank Details'), ('pan_card', 'PAN Card'), ('other', 'Other')], max_length=50),
        ),
    ]
