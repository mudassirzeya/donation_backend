# Generated by Django 3.2.5 on 2022-03-28 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_member_donation_member_info_remark_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='phone',
            new_name='username',
        ),
    ]
