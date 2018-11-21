from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from users.auths import TokenAuthentication
from users.models import PermissionLevel1

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
    authentication_classes = (TokenAuthentication, )

    def get(self, request, permission_name):
        if not request.user.is_authenticated:
            return Response({"success": False,
                             "message": "The user is unauthorized"},
                            status=HTTP_401_UNAUTHORIZED)

        user = request.user
        perm_l1 = user.permission_level1.filter(name=permission_name)
        perm_l2 = user.permission_level2.filter(name=permission_name)

        perm_l1s = PermissionLevel1.objects.filter(user=request.user)
        perm_l1_child = None
        if perm_l1s:
            for perm in perm_l1s:
                perm_l1_child = perm.permission_level2.filter(name=permission_name)

        if perm_l1 or perm_l1_child or perm_l2:
            return Response({"success": True,
                             "message": "The permission is available"},
                            status=HTTP_200_OK)

        return Response({"success": False,
                         "message": "The permission is not available"},
                        status=HTTP_403_FORBIDDEN)
