from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from ..models.mgm_class import MgmClass
from django.utils.translation import gettext as _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import NotFound


class MgmClassSerializer(serializers.ModelSerializer):
    is_archived = serializers.BooleanField(read_only=True)

    class Meta:
        model = MgmClass
        optional_fields = ['assigned_pupil', ]
        fields = [
            'id',
            'name',
            'is_archived',
            'assigned_pupil',
            'unique_name']
