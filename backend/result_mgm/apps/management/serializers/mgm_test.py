from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from ..models.mgm_test import MgmTest
from django.utils.translation import gettext as _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import NotFound


class MgmTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MgmTest
        fields = ['name',
                  'subject_id',
                  'test_date'
                  ]