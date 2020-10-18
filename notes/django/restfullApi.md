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
pip install drf-nested-routers
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

### Nested routers
> https://github.com/alanjds/drf-nested-routers

To install:
```console
pip install drf-nested-routers
```
#### Normal nested routers
##### Example
```python
# urls.py
from rest_framework_nested import routers
from views import DomainViewSet, NameserverViewSet
(...)

router = routers.SimpleRouter()
router.register(r'domains', DomainViewSet)

domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
domains_router.register(r'nameservers', NameserverViewSet, base_name='domain-nameservers')
# 'base_name' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^', include(domains_router.urls)),
)
```
```python
# views.py

## For Django' ORM-based resources ##

class NameserverViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Nameserver.objects.filter(domain=self.kwargs['domain_pk'])

## OR: non-ORM resources ##

class NameserverViewSet(viewsets.ViewSet):
    def list(self, request, domain_pk=None):
        nameservers = self.queryset.filter(domain=domain_pk)
        (...)
        return Response([...])

    def retrieve(self, request, pk=None, domain_pk=None):
        nameservers = self.queryset.get(pk=pk, domain=domain_pk)
        (...)
        return Response(serializer.data)
```

#### Hyperlinks for Nested resources


#### Infinite-depth Nesting


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
> https://blog.logrocket.com/jwt-authentication-best-practices/  
https://www.django-rest-framework.org/api-guide/authentication/  
https://stackoverflow.com/questions/31600497/django-drf-token-based-authentication-vs-json-web-token
https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html

Token authentication is appropriate for client-server setups, such as native desktop and mobile clients.

#### Installation
_\<project\>/settings.py_
```python
INSTALLED_APPS = [
  ...
  'rest_framework.authtoken'
]
```
Remember to do the migrations.
```console
python manage.py migrate
```
Include the urls in _\<project\>/urls.py_
```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
  path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
```
For clients to authenticate, the token key should be included in the `Autherization` HTTP header. The key should be prefixed by the string literal "Token", with whitespace separating the 2 strings. For example
```console
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```
**TokenAuthentication** provides the following credentials:
* `request.user`will be a Django `User`instance.
* `request.auth`will be a `rest_framework.authtoken.models.Token` instance.

#### Create token for users
For every user to have an automatically generated Token, use a _post_save_ in the _models.py_ file:
```python
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

To generate tokens for all existing users:
```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
  Token.objects.get_or_create(user=user)
```
#### Request token
The API end point is **/api-token-auth/**. This does not handle GET requests. It is a view to receive a POST request with username and password and returns the token.

To request a token:
```console
http post http://127.0.0.1:8000/api-token-auth/ username=vitor password=123
```

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

## Testing
> https://www.django-rest-framework.org/api-guide/testing/

### APIRequestFactory
Extends Django's existing `RequestFactory`class.
#### Creating test requests
The `APIRequestFactory` class supports an almost identical API to Django's standard `RequestFactory` class. This means that the standard `.get()`, `post()`, `put()`, `patch()`, `delete()`, `head()`and `options` methods are all available.
```python
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})
```

#### Forcing authentication
When testing views directly using a request factory, it's often convenient to be able to directly authenticate the request, rather than having a to construct the correct authentication credentials.
To forcibly authenticate a request, use the `force_authenticate(request, user=None, token=None)` method
```python
from rest_framework.test import force_authenticate

factory = APIRequestFactory()
user = User.objects.get(username="user")
view = AccountDetail.as_view()

request = factory.get("/accounts/django-superstars/")
force_authenticate(request, user=user)
response = view(request)
```
**Note: `force_authenticate` directly sets `request.user` to the in-memory `user` instance. If you are re-using the same `user`instance across multiple tests that update the saved `user` state, you may need to call `refresh_from_db()` between tests.**

#### Forcing CSRF validation
By default, requests created with `APIRequestFactory` will not have CSRF validation applied.
```python
factory = APIRequestFactory(enforce_csrf_checks=True)
```

### APIClient
#### Making requests
The `APIClient` class supports the same request interface as Django's standard `Client` class.
```python
from rest_framework.test import APIClient

client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')
```

#### Authenticating
##### _.login(**kwargs)_
The `login` method functions exactly as it does with Django's regular `Client` class.
```python
client = APIClient()
client.login(username='lauren', password='secret')
client.logout()
```

##### _.credentials(**kwargs)_
The `credentials` method can be used to set headers that will then be included on all subsequent requests by the test client.
```python
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

token = Token.objects.get(user__username='Juan')
client = APIClient()
client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
```
The `credentials` method is appropiate for testing APIs that require authentication headers, such as basic authentication, OAuth1a and OAuth2 authentication, and simple token authentication schemes.

##### _.force_authenticate(user=None, token=None)_
Sometimes you may want to bypass authentication entirely and force all requests by the test client to be automatically treated as authenticated.
```python
user = User.objects.get(username='Juan')
client = APIClient()
client.force_authenticate(user=user)
```

### Example
```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myproject.apps.core.models import Account

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')
```


[django-guardian]: https://github.com/django-guardian/django-guardian
