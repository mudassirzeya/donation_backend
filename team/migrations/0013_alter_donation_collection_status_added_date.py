# Generated by Django 3.2.5 on 2022-04-17 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0012_auto_20220416_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation_collection_status',
            name='added_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
