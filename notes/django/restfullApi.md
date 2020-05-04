Django Rest Framework
=====
## References
* https://www.django-rest-framework.org/
* https://www.youtube.com/watch?v=tG6O8YF91HE&t=10s
## Installation
1. Install django rest framework
```console
pip install djangorestframework
pip install markdown
pip install django-filter
```
2. Add to `INSTALLED_APPS` at _\<project\>/settings.py_
```python
INSTALLED_APPS=[
  ...
  'rest_framework',
]
```
3. Set urls for login and logout API at _\<project\>/urls.py_
```python
urlpatterns = [
  ...
  url(r'^api-auth/', include('rest_framework.urls'))
]
```


## Serializers
### Example
```python
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
```

## Views
### Example
```python
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
```

## URLs

### Router
#### Example
```python
from django.urls import include, path
from rest_framework import routers
from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

## Permissions 
> https://www.django-rest-framework.org/api-guide/permissions/

### Global policy
Add the following to \<project\>/settings.py to add global policies.
```python
REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    'rest_framework.permissions.isAuthenticated',
  ],
}
```
This sets the permission policy where:
* `'rest_framework.permissions.isAuthenticated'` is used to require the user to be authenticated. In case any one can access the api use `'rest_framework.permissions.AllowAny'` instead.

### View policy
To set the authentication policy on a per-view, or per-viewset basis:
```python
from rest_framework.permissions import isAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request, format = None):
    content = {
      'status': 'request was permitted'
    }
    return Response(content)
```

### Reference
Name                     | Description
-------------------------|------------
AllowAny                 | Allow unrestricted access
IsAuthenticated          | Deny permission to any unauthenticated user
IsAdminUser              | Deny permission unless `user.is_staff` is `True` 
IsAuthenticatedOrReadOnly| Allow unrestricted access but unauthenticated users will only be permitted if the request method is one of the "safe" methods (**GET**, **HEAD**, **OPTIONS**)
DjangoModelPermissions   | Ties into Django's standard `django.contrib.auth` model permissions. Only applies to views that have _**queryset**_ property set. <ul><li>**POST** require _**add**_ permission.</li><li>**PUT** and **PATCH** requests require _**change**_ permission.</li><li>**DELETE** requests require _**delete**_ permission.</li></ul>
DjangoModelPermissionsOrAnonReadOnly| Same as `DjangoModelPermission` but also allows unauthenicated users to have read-only access to the API.
DjangoObjectPermissions  | This ties into Django's standard _**object permission framework**_ that allows per-object permissions on models. In order to use this permission class, you need to use a permission backend that supports object-level permissions, such as [django-guardian]

### Custom permissions
Override `BasePermission` and implement:
* `.has_permission(self, request, view)`
* `.has_object_permission(self, request, view, obj)`

#### Example
```python
from rest_framework import permissions

class BlackListPermission(permission.BasePermission):
  def has_permission(self, request, view):
    ip_addr = request.META["REMOTE_ADDR"]
    blacklisted = Blacklist.objects.filter(ip_address=ipd_addr).exists()
```

## Authentication
> https://www.django-rest-framework.org/api-guide/authentication/

REST framework will attempt to authenticate with each class in the list, and will set `request.user` and `request.auth`using the return value of the first class that successfully authenticates.

If no class authenticates, `request.user` will be set to an instance of `django.contrib.auth.models.AnonymousUser`and `request.auth` will be set to `None`.

Authentications always runs at the very start of the view, before the permission and throttling checks occur.

When an unauthenticated request is denied permission there are two different error codes that may be appropiate
* **HTTP 401 Unauthorized**: always include a _www-Authenticate_ header, that instructs the client how to authenticate.
* **HTTP 403 Permission Denied** does not include a _www-Authenticate_ header.

### Global policy
To set the default authentication schemes globally, write in _\<project\>/settings.py_
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

### View policy
You can also set the authentication scheme on a per-view or per-viewset basis
```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
```

### Basic Authentication
This scheme uses **HTTP Basic Authentication**, signed against a user's username and password. **Only appropriate for testing.**

If successfully authenticated, `BasicAuthentication` provides the following credentials:
* `request.user` will be a Django `User` instance.
* `request.auth` will be a `None`

Unauthenticated responses that are denied permission will result in an `HTTP 401 Unauthorized` response with an appropiate WWW-Authenticate header.

### Token Authentication
<div style="text-align:center;font-size:1.2rem;font-weight:bold;">Check jwt notes!!</div>

### SessionAuthentication
This authentication scheme uses Django's default session backend for authentication. This is appropiate for AJAX clients that are running in the same session context as your website.

If successfully authenticated, `SessionAuthentication` provides the following credentials.
* `request.user` will be a Django User instance.
* `request.auth` will be None.

Unauthenticated responses that are denied permission will result in an **HTTP 403 Forbidden response**.

If using an AJAX style API with SessionAuthentication, make sure you include a valid _CSRF token_ for any "unsafe" HTTP method calls, such as **PUT**, **PATCH**, **POST**, **DELETE** requests.

## Settings
### Pagination
> https://www.django-rest-framework.org/api-guide/pagination/

Pagination allows you to control how many objects per page are returned. In _\<project\>/settings.py_:
```python
REST_FRAMEWORK = {
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE': 10
}
```
#### Request
```
GET https://api.example.org/accounts/?page=4
```

#### Response
```json
HTTP 200 OK{
  "count": 1023,
  "next": "https://api.example.org/accounts/?page=5",
  "previous": "https://api.example.org/accounts/?page=3",
  "results": [
    ...
  ]
}
```

[django-guardian]: https://github.com/django-guardian/django-guardian
