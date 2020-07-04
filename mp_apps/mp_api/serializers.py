from rest_framework import serializers
from mp_apps.mp_api.models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'client_member_id', 'account_id']
