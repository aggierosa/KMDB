from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializer import LoginSerializer, UserSerializer

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserAuthView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()

        result_page = self.paginate_queryset(users, request, self)

        serializer = UserSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

        # paginação

class UserDetailAuthView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return Response(
                {"message": "Usuário não encontrado"}
            )

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response ({"token": token.key})

        return Response ({"message": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED)