import os

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .services.pdf_to_excel import convert_pdf_to_excel

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    userID = request.data.get("userID")
    password = request.data.get("password")

    if userID is None or password is None:
        return Response({'error': 'Please provide both userID and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, userID=userID, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)

    payload = jwt_payload_handler(user)
    jwt_token = jwt_encode_handler(payload)
    return Response({'token': jwt_token}, status=status.HTTP_200_OK)


@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        file_name = fs.save(uploaded_file.name, uploaded_file)
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # PDFファイルをExcelファイルに変換
        excel_file_path = convert_pdf_to_excel(pdf_file_path)  # ここで関数を利用します。

        # Excelファイルをレスポンスとして返す
        with open(excel_file_path, 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=output.xlsx'
            return response
