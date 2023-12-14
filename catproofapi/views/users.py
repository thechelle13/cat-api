from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from catproofapi.models import CatUser 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]
        extra_kwargs = {"password": {"write_only": True}}


class CatUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CatUser
        fields = ("user", "active",  "bio")


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=["get"], url_path="catusers")
    def get_cat_users(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Filter CatUser objects for the current authenticated user
        cat_user = CatUser.objects.filter(user=request.user).first()

        # Check if the CatUser exists
        if cat_user:
            serializer = CatUserSerializer(cat_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "CatUser not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"], url_path="register")
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                email=serializer.validated_data["username"],
                #email=serializer.validated_data["email"],
            )
            cat_user = CatUser.objects.create(
                user=user,
                active=True,
                bio= request.data.get("bio"),
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def user_login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token = Token.objects.get(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
