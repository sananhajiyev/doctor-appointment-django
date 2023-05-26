from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from jwt import decode

from .serializers import UserSerializer
from .models import User
from backend.settings import SECRET_KEY

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user=User.objects.get(email=serializer.data['email'])

        refresh_token = RefreshToken.for_user(user=user)
        
        response = Response()

        response.set_cookie(key='refreshToken', value=str(refresh_token), httponly=True)

        response.data = {
            'token': str(refresh_token.access_token)
        }

        group = Group.objects.get(name='Employee')

        group.user_set.add(user)

        return response


class LoginView(APIView):
    def post(self, request):
        user = User.objects.get(email=request.data['email'])

        if not user:
            raise APIException(_('Invalid email'))
        
        if not user.check_password(request.data['password']):
            raise APIException(_('Invalid password'))

        refresh_token = RefreshToken.for_user(user)
        
        response = Response()

        response.set_cookie(key='refreshToken', value=str(refresh_token), httponly=True)

        response.data = {
            'token': str(refresh_token.access_token)
        }

        return response

class UserAPIView(APIView):
    def get(self, request):
        auth = JWTAuthentication()
        user, token = auth.authenticate(request=request)
        if not user:
            raise AuthenticationFailed(_('Could not authenticate'))
        data = self.get_user_json(user)
        return Response(data)

    def get_user_json(self, user):
        data = {}
        raw = UserSerializer(user).data
        data['is_employee'] = user.groups.filter(name='Employee').exists()
        data['id'] = raw['id']
        data['first_name'] = raw['first_name']
        data['last_name'] = raw['last_name']
        data['age'] = raw['age']
        data['phone_number'] = raw['phone_number']
        data['is_employee'] = raw['is_employee']
        data['email'] = raw['email']
        data['gender'] = raw['gender']
        return data

class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        auth = JWTAuthentication()
        
        try:
            user = auth.get_user(decode(jwt=refresh_token, key=SECRET_KEY, algorithms=['HS256']))
        except:
            raise AuthenticationFailed(_('Could not authenticate'))


        refresh_token = RefreshToken.for_user(user)

        response = Response()

        response.set_cookie(key='refreshToken', value=str(refresh_token), httponly=True)

        response.data = {
            'token': str(refresh_token.access_token)
        }

        return response

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = RefreshToken(request.COOKIES.get('refreshToken'))
        token.blacklist()

        response = Response()
        response.delete_cookie(key='refreshToken')
        response.status_code = 200
        return response
