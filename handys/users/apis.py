from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from users.models import PermissionLevel1, PermissionLevel2

User = get_user_model()


@csrf_exempt
@api_view(["POST"])
def login(request):
    """
    Authenticate user with email and password, and response with token
    """
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({"success": False,
                         "message": "Please input email and password"},
                        status=HTTP_400_BAD_REQUEST)
    user = User.objects.filter(email=email, password=password).first()
    if user:
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"success": True,
                         "message": "Login succeed",
                         "token": token.key},
                        status=HTTP_200_OK)
    return Response({"success": False,
                     "message": "The user does not found"},
                    status=HTTP_404_NOT_FOUND)


@api_view(["GET"])
def check_permission(request, permission_name):
    """
    Check the existence and activity of permission
    """
    permission_lv1 = PermissionLevel1.objects.filter(name=permission_name)
    permission_lv2 = PermissionLevel2.objects.filter(name=permission_name)

    if permission_lv1 or permission_lv2:
        return Response({"success": True,
                         "message": "The permission is available"},
                        status=HTTP_200_OK)

    return Response({"success": False,
                     "message": "The permission does not exist"},
                    status=HTTP_404_NOT_FOUND)
