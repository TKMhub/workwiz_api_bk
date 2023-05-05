from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

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
