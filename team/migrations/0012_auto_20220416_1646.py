# Generated by Django 3.2.5 on 2022-04-16 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0011_member_donation_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation_collection_status',
            name='amount',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='member_donation',
            name='amount',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
