from rest_framework import status, viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from mp_apps.mp_api.models import Member
from mp_apps.mp_api.serializers import FileSerializer, MemberSerializer

from .tasks import load_data


class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Members to be viewed or edited.
    """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filterset_fields = (
        "account_id",
        "phone_number",
        "client_member_id",
    )


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            load_data.delay(file_serializer.data.get("file"))
            #print("after load data")
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
