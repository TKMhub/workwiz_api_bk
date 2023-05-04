from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nickname(request):
    access_token = AccessToken.for_user(request.user)
    return Response({'nickname': request.user.username, 'access_token': str(access_token)})
