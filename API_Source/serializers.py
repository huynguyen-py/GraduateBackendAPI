from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True, required=False)
    email = serializers.EmailField(max_length=255, min_length=4, required=False)
    first_name = serializers.CharField(max_length=255, min_length=2, required=False)
    last_name = serializers.CharField(max_length=255, min_length=2, required=False)

    # diagnosisrecord = serializers.PrimaryKeyRelatedField(many=True, queryset=DiagnosisRecord.objects.all())

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email'
            , 'is_active', 'is_staff', 'is_superuser', 'is_verified'
            , 'create_at', 'user_permissions', 'avatar', 'phone', 'address', 'Followed']

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
            },
            'avatar': {
                'required': False,
            },
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric character"
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already in use'}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def __str__(self):
        return self.username


class EmailVertificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=13)
    password = serializers.CharField(max_length=68, min_length=1, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=500, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens(),
        }
