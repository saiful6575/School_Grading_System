from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from ..models.users import User
from django.utils.translation import gettext as _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import NotFound


class RegistrationUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField(required=False)
    is_active = serializers.BooleanField(default=True)
    is_teacher = serializers.BooleanField(default=False)
    is_student = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    password = serializers.CharField(write_only=True,read_only=False)

    class Meta:
        model = User
        optional_fields = ['phone_number',]
        fields = ['id',
            'username',
                  'name',
                  'email', 'phone_number', 'is_active', 'is_superuser', 'is_teacher', 'is_student', 'password']


    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        instance.is_superuser = validated_data.get('is_superuser', False)
        instance.is_student = validated_data.get('is_student', False)
        instance.is_teacher = validated_data.get('is_teacher', False)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        new_password = validated_data.pop('password', None)
        if new_password:
            instance.set_password(new_password)
            instance.save()
        instance.phone_number = validated_data.get('phone_number', '')
        instance.email = validated_data.get('email', '')
        instance.name = validated_data.get('name', '')
        instance.is_superuser = validated_data.get('is_superuser', False)
        instance.is_student = validated_data.get('is_student', False)
        instance.is_teacher = validated_data.get('is_teacher', False)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=150, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    phone_number = serializers.CharField(max_length=100, read_only=True, required=False)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user_data = User.objects.filter(email__iexact=email.strip().lower())
        if len(user_data) <= 0:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        user = authenticate(username=user_data[0].email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        role = 'STUDENT'
        if user.is_superuser:
            role = 'ADMIN'
        elif user.is_teacher:
            role = 'TEACHER'
        return {
            'email': user.email,
            'name': user.name,
            'role': role,
            'phone_number': user.phone_number,
            'token': user.token
        }
