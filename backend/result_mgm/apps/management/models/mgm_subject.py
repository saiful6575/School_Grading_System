from django.db import models
from result_mgm.apps.authentication.models.users import User
from result_mgm.apps.management.models.mgm_class import MgmClass
import random


def create_new_ref_number():
    not_unique = True
    while not_unique:
        unique_ref = "SUB-" + str(random.randint(1000000000, 9999999999))
        if not MgmSubject.objects.filter(unique_name=unique_ref):
            not_unique = False
    return unique_ref


class MgmSubject(models.Model):
    name = models.CharField("Name", max_length=300, blank=True, null=True)
    assigned_teacher = models.ForeignKey(User, related_name="assigned_teacher_ids",
                       on_delete=models.SET_NULL, blank=True, null=True )
    class_id = models.ForeignKey(MgmClass, related_name="mgm_class_subject_ids",
                       on_delete=models.SET_NULL, blank=True, null=True )
    unique_name = models.CharField("Unique Name",
                                   max_length=20,
                                   blank=True,
                                   editable=False,
                                   unique=True,
                                   default=create_new_ref_number)
    is_archived = models.BooleanField("Is Archived", default=False)