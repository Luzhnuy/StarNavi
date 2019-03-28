from django.contrib.auth.models import User
from django.conf import settings
from .models import Post
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status,viewsets
from rest_framework_jwt.utils import jwt_payload_handler
from .serializers import UserSerializer, PostSerializer
from rest_framework.response import Response
from .likes_function import *
from .mixins import LikedMixin

class UserList(APIView):
    permission_classes=(AllowAny, )

    def get(self,request,format=None):
        users=User.objects.all()
        users=UserSerializer(users,many=True)
        return Response(users.data)

class UserDetali(APIView):
    permission_classes=[AllowAny, ]

    def get(self,request,pk,format=None):
        try: 
            user=User.objects.get(pk=pk)
        except User.DoesNotExist:
            user_count=User.objects.all().count()
            user=User.objects.get(pk=user_count)
        user=UserSerializer(user)
        return Response(user.data)


class UserCreate(APIView):
    permission_classes=(AllowAny, )

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                data = serializer.data
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
 
    try:
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            user = 0
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
 
            except Exception as e:
                raise e

        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a username and a password'}
        return Response(res)



class UserRetrieveUpdate(RetrieveUpdateAPIView):
 
   
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
 
    def get(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(request.user)
 
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
 
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
 
        return Response(serializer.data, status=status.HTTP_200_OK)




class PostViewSet(LikedMixin,viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=(IsAuthenticated,)

