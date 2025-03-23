from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):

        pw = validated_data["password"]
        repeated_password = validated_data["repeated_password"]
        email = validated_data["email"]

        if (pw != repeated_password):
            raise serializers.ValidationError("Password stimmt nicht überein")

        if (User.objects.filter(email=validated_data["email"])):
            raise serializers.ValidationError("Diese Email gibt es bereits")

        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user