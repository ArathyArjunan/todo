from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from reminder_api.serializers import UserSerializer


class UserCreationView(APIView):
    def post(self,request,*args, **kwargs):
        serializer=UserSerializer(data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

