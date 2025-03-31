from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from .serializers import RegistrationSerializer
from django.contrib.auth.models import User

class RegistrationView(APIView):
	permission_classes = [AllowAny]

	data = {}

	def post(self, request):
		serializer = RegistrationSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()

			token, created = Token.objects.get_or_create(user=user)

			data = {
				"token": token.key,
				"username": user.username,
				"email": user.email
			}
			return Response(data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
	permission_classes = [AllowAny]

	data = {}

	def post(self, request):

		email = request.data["email"]
		pw = request.data["password"]

		user = authenticate(username=email, password=pw)

		if user is None:
			return Response({"error": "Ungültige E-Mail oder Passwort"}, status=status.HTTP_400_BAD_REQUEST)

		token, created = Token.objects.get_or_create(user=user)

		data = {
				"token": token.key,
				"username": user.username,
				"email": user.email
			}

		return Response(data, status=status.HTTP_201_CREATED)

class GuestProfile(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        guest_username = "Guest"
        guest_user, created = User.objects.get_or_create(username=guest_username, is_active=True)
        Token.objects.filter(user=guest_user).delete()
        token = Token.objects.create(user=guest_user)

        data = {
            "token": token.key,
            "username": guest_user.username,
        }

        return Response(data, status=status.HTTP_201_CREATED)