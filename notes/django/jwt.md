Django JSON Web Token
====
> https://simpleisbetterthancomplex.com/tutorial/2018/12/19/how-to-use-jwt-authentication-with-django-rest-framework.html

The JWT is acquried by exchanging an username + password for an **access token** (expiresin 5 mins) and an **refresh token** (expires in 24 hours)

## Structure
This information is encoded using **BASE64**

### Header
```json
{
  "typ": "JWT",
  "alg": "HS256"
}
```

### Payload
```json
{
  "token_type": "access",
  "exp": 1543828431,
  "jti": "7f5997b7150d46579dc2b49167097e7b",
  "user_id": 1
}
```

### Signature
The signature is issued by the JWT backend, using the header base64 + payload base64 + **SECRET_KEY**. If any information in the header or in the payload was changed by the client it will invalidate the signature!


## Installation

```console
pip install djangorestframework_simplejwt
```
### _\<project\>/settings.py_:
```python
REST_FRAMEWORK = {
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework.simplejwt.authentication.JWTAuthentication',
  ],
}
```

### _\<project\>/urls.py_
```python
from django.urls import path
from rest_framework_simple_jwt import views as jwt_views

urlpatterns = [
  path("api/token/", jwt_views.TokenObtainPairView.as_view(), name="toke_obtain_pair"),
  path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh")
]
```

## Obtain and Refresh Token
First step is to authenticate and obtain the token.
```console
https post http://localhost:8000/api/token/ username="user" password=123
```
Your response is going to look like this:
![token response][token_resp]
**STORE BOTH THE _ACCESS TOKEN_ AND THE _REFRESH TOKEN_ ON THE CLIENT SIDE.** Usually in the [local storage].

In order to access the protected views on the backend use the _access token_
```console
http http://127.0.0.1:8000/hello/ "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQ1MjI0MjAwLCJqdGkiOiJlMGQxZDY2MjE5ODc0ZTY3OWY0NjM0ZWU2NTQ2YTIwMCIsInVzZXJfaWQiOjF9.9eHat3CvRQYnb5EdcgYFzUyMobXzxlAVh_IAgqyvzCE"
```

**You can use this _access token_ for the next five minutes**. Then you need to refresh your token

```console
http post http://127.0.0.1:8000/api/token/refresh/ refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU0NTMwODIyMiwianRpIjoiNzAyOGFlNjc0ZTdjNDZlMDlmMzUwYjg3MjU1NGUxODQiLCJ1c2VyX2lkIjoxfQ.Md8AO3dDrQBvWYWeZsd_A1J39z6b6HEwWIUZ7ilOiPE
```
The return is a new _access token_ that you should use in the subsequent requests.

The _refresh_token_ is valid for the next 24 hours. Then the user will need to perform a full authentication to get a new set of _access token_ and _refresh_token_.



[token_resp]: ../img/jwt_tokenExample.png
[local storage]: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
