from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    USERTYPE = (
        ('app_user', 'app_user'),
        ('admin', 'admin'),
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    user_type = models.CharField(max_length=100, blank=True, choices=USERTYPE)
    date_of_joining = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Member_Profile_Photo(models.Model):
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)


class Member_Info(models.Model):
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    map_lat = models.CharField(max_length=100, null=True, blank=True)
    map_lon = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=1000, null=True, blank=True)


class Remark_Member(models.Model):
    remark_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        Member_Info, null=True, blank=True, on_delete=models.CASCADE)
    report_note = models.CharField(max_length=500, null=True, blank=True)
    added_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)


class Member_Donation(models.Model):
    received_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        Member_Info, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=500, null=True, blank=True)
    added_date = models.DateTimeField(blank=True, null=True)
