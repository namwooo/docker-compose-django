# docker-compose-django

API server to obtain token and check permission, and deploy with docker-compose.

## 01. How To Start docker-compose-django

Clone the application

```
git clone git@github.com:namwooo/docker-compose-django.git
```

Start with docker-compose at root folder of the application

```
docker-compose up
```

Stop application and remove docker-compose

```
docker-compose down
```

## 02. Technical Stack

```
python 3.7.0
django 2.1.3
django REST Framework 3.9.0
uWSGI 2.0.17.1
NGINX 1.15.6
postgresql 9.5
docker 18.06.1
```

## 03. API

### Obtain Token

```
POST /users/token HTTP/1.1
Content_Type: application/json
```

Obtain Token_request body

```
{
	'email': 'namwoo@test.com',
	'password': 'test_password'
}
```

### Check Permission

```
GET /users/permission/{permission_name} HTTP/1.1
```

Check Permission_header

```
Authorization Bearer: <access_token>
```
