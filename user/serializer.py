from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'gender', 'age']

    # field level validation
    def validate_age(self, value):
        return value


    def validate(self, data):

        if data['age'] < 18:
            raise serializers.ValidationError("age must be greater than 18 to open account")
        return data


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


