from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from ..models.mgm_test_participant import MgmTestParticipant
from result_mgm.apps.management.serializers.mgm_test_participant import MgmTestParticipantSerializer
# Create your views here.


class MgmTestParticipantAPI(ModelViewSet):

    lookup_field = 'id'
    queryset = MgmTestParticipant.objects.all()
    serializer_class = MgmTestParticipantSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.user and request.user.is_superuser:
            return Response({'status': True, 'output': MgmTestParticipantSerializer(MgmTestParticipant.objects.all(),many=True).data}, status=status.HTTP_200_OK)
        elif request.user and request.user.is_teacher:
            return Response({'status': True, 'output': MgmTestParticipantSerializer(MgmTestParticipant.objects.all(),many=True).data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None):
        try:
            if request.user and request.user.is_superuser:
                return Response({'status': True, 'output': MgmTestParticipantSerializer(MgmTestParticipant.objects.get(id=id),many=False).data}, status=status.HTTP_200_OK)
            return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid User information found'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                user = request.data.get('test-participant', {})
                get_staff = MgmTestParticipant.objects.get(id=id)
                serializer = self.serializer_class(get_staff, data=user, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'result': 'success',
                        "output": serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'result': 'error',
                        'output': {},
                        'message': serializer.errors,

                    }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid User information found'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            if request.user and request.user.is_superuser:
                user = request.data.get('test-participant', {})
                serializer = self.serializer_class(data=user)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'result': 'success',
                        "output": serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'result': 'error',
                        'output': {},
                        'message': serializer.errors,

                    }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid User information found'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                test_participant_info = MgmTestParticipant.objects.get(id=id)
                if test_participant_info:
                    test_participant_info.delete()
                    return Response({
                        'result': 'success',
                        "output": "Test Participant deleted successfully"
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'result': 'success',
                        "output": "Test Participant not found"
                    }, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': False, 'output': 'Test Participant not found'}, status=status.HTTP_400_BAD_REQUEST)
