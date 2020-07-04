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

    def get_queryset(self):
        """
        Optionally restricts the returned Members based on url params, by filtering against account_id, phone_number and client_member_id
        """
        queryset = Member.objects.all()
        account_id = self.request.query_params.get('account_id', None)
        phone_number = self.request.query_params.get('phone_number', None)
        client_member_id = self.request.query_params.get('client_member_id', None)

        if account_id is not None:
            queryset = queryset.filter(account_id=account_id)

        if phone_number is not None:
            queryset = queryset.filter(phone_number=phone_number)

        if client_member_id is not None:
            queryset = queryset.filter(client_member_id=client_member_id)

        return queryset
