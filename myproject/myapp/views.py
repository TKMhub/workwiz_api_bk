from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from .utils import pdf_to_excel
from .serializers import MyTokenObtainPairSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nickname(request):
    user = request.user
    return Response({"nickname": user.nickname})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def post(request, *args, **kwargs):
    pdf_file = request.FILES['file']
    if not pdf_file.name.lower().endswith('.pdf'):
        return Response({"error": "Invalid file format. Please upload a PDF file."},
                        status=status.HTTP_400_BAD_REQUEST)

    output_file = f"{pdf_file.name.split('.')[0]}.xlsx"
    converted_file_path = pdf_to_excel(pdf_file.temporary_file_path(), output_file)

    response = FileResponse(open(converted_file_path, 'rb'), content_type='application/vnd.openxmlformats'
                                                                          '-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={output_file}'
    return response


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
