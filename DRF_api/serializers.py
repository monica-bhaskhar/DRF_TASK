from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def validate(self, attrs):
        if len(attrs.get('password')) > 8:
            raise serializers.ValidationError("Password should not be greater than 8 !")

        queryset = User.objects.filter(email=attrs.get('email')).exists()
        if queryset:
            raise serializers.ValidationError("Email Already Exist!")

        attrs['password'] = make_password(attrs['password'])
        return attrs    

class UserLoginSerializer(serializers.Serializer):
    # username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.'),
        'invalid_user' : _('Invalid User Email.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        query = User.objects.filter(email=attrs.get("email")).exists()
        if query:
            username = User.objects.get(email=attrs.get("email"))
            user_val = authenticate(username=username, password=attrs.get('password'))

            self.user = authenticate(username=username, password=attrs.get('password'))
            if self.user:
                if not self.user.is_active:
                    raise serializers.ValidationError(self.error_messages['inactive_account'])
                return attrs
            else:
                raise serializers.ValidationError(self.error_messages['invalid_credentials'])
        else:
            raise serializers.ValidationError(self.error_messages['invalid_user'])



class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")

class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ("id","title", "status")