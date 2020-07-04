from rest_framework import serializers

from mp_apps.mp_api.models import File, Member


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "client_member_id",
            "account_id",
        ]


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ["file"]
