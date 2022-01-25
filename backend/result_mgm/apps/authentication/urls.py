from django.conf.urls import url, include
from rest_framework import routers
from .views import (
    LoginUserAPI, UserAPI
)



router = routers.SimpleRouter()
router.register('users', UserAPI, basename="UserAPI")
urlpatterns = [
    url(r'^login/?$', LoginUserAPI.as_view()),
    url(r'^', include(router.urls)),
]