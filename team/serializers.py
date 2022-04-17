from rest_framework.serializers import ModelSerializer
from .models import Member_Info, Remark_Member, Member_Donation, Presentation
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member_Info
        fields = '__all__'


class RemarkSerializer(ModelSerializer):
    class Meta:
        model = Remark_Member
        fields = '__all__'


class DonationSerializer(ModelSerializer):
    class Meta:
        model = Member_Donation
        fields = '__all__'


class PresentationSerializer(ModelSerializer):
    class Meta:
        model = Presentation
        fields = '__all__'
