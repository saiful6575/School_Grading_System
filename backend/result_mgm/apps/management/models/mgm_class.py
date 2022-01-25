from django.db import models
from result_mgm.apps.authentication.models.users import User
import random


def create_new_ref_number():
    not_unique = True
    while not_unique:
        unique_ref = "CLASS-" + str(random.randint(1000000000, 9999999999))
        if not MgmClass.objects.filter(unique_name=unique_ref):
            not_unique = False
    return unique_ref


class MgmClass(models.Model):
    name = models.CharField("Name", max_length=300, blank=True, null=True)
    assigned_pupil = models.ManyToManyField(User, related_name="pupil_class_ids", blank=True, null=True )
    is_archived = models.BooleanField("Is Archived", default=False)
    unique_name = models.CharField("Unique Name",
                                   max_length=20,
                                   blank=True,
                                   editable=False,
                                   unique=True,
                                   default=create_new_ref_number)
