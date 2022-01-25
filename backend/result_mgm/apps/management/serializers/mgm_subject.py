from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from ..models.mgm_subject import MgmSubject
from django.utils.translation import gettext as _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import NotFound


class MgmSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = MgmSubject
        fields = ['id',
                  'name',
                  'assigned_teacher',
                  'class_id',
                  'unique_name',
                  'is_archived',
                  ]