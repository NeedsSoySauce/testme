from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers

from .exceptions import UsernameUnavailableException, EmailInUseException
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(max_length=32, min_length=2)
    email = serializers.EmailField(required=False, allow_null=True, default=None)
    password = serializers.CharField(max_length=128, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password']

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
        except IntegrityError as e:
            message = str(e)
            if 'username' in message:
                raise UsernameUnavailableException()
            elif 'email' in message:
                raise EmailInUseException()
            else:
                raise

        return user
