import os
import pandas as pd
import io
import pdfplumber

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
import tempfile


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

    # Create a temporary file and write the uploaded file's content to it.
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in pdf_file.chunks():
            temp_file.write(chunk)

    dfs = []
    with pdfplumber.open(temp_file.name) as pdf:
        for page in pdf.pages:
            table = page.extract_table()  # Extract the table
            if table:
                dfs.append(pd.DataFrame(table[1:], columns=table[0]))

    # Don't forget to remove the temporary file when you're done with it.
    os.unlink(temp_file.name)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        if not dfs:
            # If no tables were extracted from the PDF, create an empty sheet.
            writer.book.create_sheet("No Tables Extracted")
        else:
            for i, df in enumerate(dfs):
                df.to_excel(writer, sheet_name=f'Page {i + 1}', index=False)
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename='converted.xlsx')

    return response
