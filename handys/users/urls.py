from django.urls import path

from users.apis import CheckPermission, ObtainToken

urlpatterns = [
    path('token/', ObtainToken.as_view()),
    path('permission/<slug:permission_name>/', CheckPermission.as_view()),
]