from django.conf.urls import url, include
from rest_framework import routers
from .views import (
    MgmClassAPI, MgmSubjectAPI, MgmTestParticipantAPI, MgmTestAPI
)



router = routers.SimpleRouter()
router.register('class', MgmClassAPI, basename="MgmClassAPI")
router.register('subject', MgmSubjectAPI, basename="MgmSubjectAPI")
router.register('test-participant', MgmTestParticipantAPI, basename="MgmTestParticipantAPI")
router.register('test', MgmTestAPI, basename="MgmTestAPI")
urlpatterns = [
    url(r'^', include(router.urls)),
]