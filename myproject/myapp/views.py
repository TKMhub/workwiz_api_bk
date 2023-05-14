import os

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import tabula
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import pandas as pd
import io


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

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def convert_pdf_to_excel(request):
    pdf_file = request.FILES['pdf']
    dfs = tabula.read_pdf(pdf_file.temporary_file_path(), pages='all')

    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            for i, df in enumerate(dfs):
                df.to_excel(writer, sheet_name=f'Page {i + 1}', index=False)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='converted.xlsx')
