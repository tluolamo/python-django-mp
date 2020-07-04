from rest_framework import viewsets
from mp_apps.mp_api.serializers import MemberSerializer, FileSerializer
from mp_apps.mp_api.models import Member, File
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import mixins
from rest_framework import generics
from django.http import JsonResponse

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Members to be viewed or edited.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filterset_fields = ('account_id', 'phone_number', 'client_member_id', )


# class FileUploadViewSet(viewsets.ModelViewSet):
#     """upload file"""
#     queryset = FileUpload.objects.all()
#     serializer_class = FileUploadSerializer
#     parser_classes = (MultiPartParser, FormParser,)
#
#     def perform_create(self, serializer):
#         serializer.save(datafile=self.request.data.get('datafile'))
#
# class CsvUploadParser(FileUploadParser):
#     media_type = 'text/plain'
#
#
# class MembersBatchUploadView(APIView):
#     """
#     API endpoint that allows upload of a CSV file to batch load members
#     """
#     parser_class = (FileUploadParser)
#
#     def put(self, request, format=None, filename=None):
#         file_serializer = FileSerializer(data=request.data)
#
#         if file_serializer.is_valid():
#           file_serializer.save()
#           return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#           return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        # print(filename)
        # file_obj = request.data['file']
        # print(file_obj)
        # ...
        # do some stuff with uploaded file
        # ...
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #return JsonResponse({ "response": "success" }, status=204)
