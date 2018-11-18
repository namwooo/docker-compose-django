from django.urls import path

from users.apis import login, check_permission

urlpatterns = [
    path('api/login', login),
    path('api/permission/<slug:permission_name>/', check_permission),
]