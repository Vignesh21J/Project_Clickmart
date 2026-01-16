from rest_framework import serializers

# from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["id", "email", "first_name", "last_name", "username"]
        read_only_fields = ["id", "email"]