from django.contrib.auth.models import User
from .models import Post
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer, PostSerializer
from rest_framework.response import Response


class UserList(APIView):
    
    def get(self,request,format=None):
        users=User.objects.all()
        users=UserSerializer(users,many=True)
        return Response(users.data)

class UserDetali(APIView):

    def get(self,request,pk,format=None):
        try: 
            user=User.objects.get(pk=pk)
        except User.DoesNotExist:
            user_count=User.objects.all().count()
            user=User.objects.get(pk=user_count)
        user=UserSerializer(user)
        return Response(user.data)


class UserCreate(APIView):

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                data = serializer.data
                data['token'] = token.key
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)