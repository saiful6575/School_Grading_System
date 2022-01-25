from django.db import models
from .mgm_test import MgmTest
from result_mgm.apps.authentication.models.users import User
import random

class MgmTestParticipant(models.Model):
    test_id = models.ForeignKey(MgmTest, related_name="test_participant_ids", blank=True, null=True, on_delete=models.SET_NULL )
    pupil_id = models.ForeignKey(User, related_name="pupil_test_ids", blank=True, null=True, on_delete=models.SET_NULL)
    grade = models.DecimalField("Grade", blank=True, null=True, decimal_places=2, max_digits=8)
