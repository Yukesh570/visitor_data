# Generated by Django 5.1 on 2024-08-23 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0009_visitor_data_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor_data',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
