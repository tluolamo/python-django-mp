from rest_framework import viewsets
from mp_apps.mp_api.serializers import MemberSerializer
from mp_apps.mp_api.models import Member
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Members to be viewed or edited.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filterset_fields = ('account_id', 'phone_number', 'client_member_id', )
