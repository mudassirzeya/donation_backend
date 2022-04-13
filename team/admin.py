from django.contrib import admin
from .models import UserProfile, Member_Info, Remark_Member, Member_Donation
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Member_Info)
admin.site.register(Remark_Member)
admin.site.register(Member_Donation)
