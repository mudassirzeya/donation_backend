# Generated by Django 3.2.5 on 2022-04-14 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0009_member_donation_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation_Collection_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('note', models.CharField(blank=True, max_length=500, null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('given_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('given_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_model', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Member_Profile_Photo',
        ),
    ]
