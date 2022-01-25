import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models



class UserManager(BaseUserManager):

    def create_user(self, user_name=None, email=None, password=None, name=None, **kw):
        if name is None:
            name = email
        if email is None:
            raise TypeError('Email is not triggered')
        phone_number = '' if 'phone_number' not in kw.keys() or kw['phone_number'] is None else kw['phone_number']

        user = self.model(name=name, email=self.normalize_email(email.strip().lower()), phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username=None, email=None, password=None, name=None, **kw):
        if password is None:
            raise TypeError('Error occured in password')
        if name == None:
            name = email
        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=False, blank=True)
    name = models.CharField(db_index=True, max_length=150)
    email = models.EmailField(db_index=True, unique=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    temporary_password_generate = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def card_token(self):
        return ""

    def get_full_name(self):
        self.name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(weeks=30)
        token = jwt.encode({
            'email': self.email,
            'password': self.password,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

