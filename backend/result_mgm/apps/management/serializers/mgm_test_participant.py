from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from ..models.mgm_test_participant import MgmTestParticipant
from django.utils.translation import gettext as _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import NotFound


class MgmTestParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = MgmTestParticipant
        fields = ['test_id',
                  'pupil_id',
                  'grade'
                  ]