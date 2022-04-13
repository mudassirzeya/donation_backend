from rest_framework.serializers import ModelSerializer
from .models import Member_Info, Remark_Member, Member_Donation
# from rest_framework.authtoken.models import Token


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
