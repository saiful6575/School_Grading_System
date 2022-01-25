from django.db import models
from .mgm_subject import MgmSubject
import random

class MgmTest(models.Model):
    name = models.CharField("Name", max_length=300, blank=True, null=True)
    subject_id = models.ForeignKey(MgmSubject, related_name="subject_test_ids",
                 on_delete=models.SET_NULL, blank=True, null=True )
    test_date = models.DateField("Test Date", blank=True, null=True)