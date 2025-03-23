from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from .serializers import RegistrationSerializer

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