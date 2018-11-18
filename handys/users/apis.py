from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from users.auths import TokenAuthentication
from users.models import PermissionLevel1, PermissionLevel2

User = get_user_model()


class ObtainToken(APIView):
    """
    Obtain token with authenticating email and password
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({"success": False,
                             "message": "Please input email and password"},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"success": True,
                             "message": "Login succeed",
                             "token": token.key},
                            status=HTTP_200_OK)
        return Response({"success": False,
                         "message": "The user does not found"},
                        status=HTTP_404_NOT_FOUND)


class CheckPermission(APIView):
    """
    Check the existence and activity of permission

    * Requires token authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, permission_name):
        permission_lv1 = PermissionLevel1.objects.filter(name=permission_name)
        permission_lv2 = PermissionLevel2.objects.filter(name=permission_name)

        if permission_lv1 or permission_lv2:
            return Response({"success": True,
                             "message": "The permission is available"},
                            status=HTTP_200_OK)

        return Response({"success": False,
                         "message": "The permission does not exist"},
                        status=HTTP_404_NOT_FOUND)
