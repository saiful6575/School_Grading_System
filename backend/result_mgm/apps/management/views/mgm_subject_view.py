from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from ..models.mgm_subject import MgmSubject
from result_mgm.apps.management.serializers.mgm_subject import MgmSubjectSerializer
# Create your views here.


class MgmSubjectAPI(ModelViewSet):

    lookup_field = 'id'
    queryset = MgmSubject.objects.all()
    serializer_class = MgmSubjectSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.user and request.user.is_superuser:
            return Response({'status': True, 'output': MgmSubjectSerializer(MgmSubject.objects.all(),many=True).data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'output': 'Please provide valid Subject information to access data.'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None):
        try:
            if request.user and request.user.is_superuser:
                return Response({'status': True, 'output': MgmSubjectSerializer(MgmSubject.objects.get(id=id),many=False).data}, status=status.HTTP_200_OK)
            return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid Subject information found'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                user = request.data.get('subject', {})
                get_staff = MgmSubject.objects.get(id=id)
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
            return Response({'status': False, 'output': 'No Valid Subject information found'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            if request.user and request.user.is_superuser:
                user = request.data.get('subject', {})
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
            return Response({'status': False, 'output': 'No Valid Subject information found'}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                subject_info = MgmSubject.objects.get(id=id)
                if not subject_info.is_archived and subject_info.subject_test_ids.count() <=0:
                    subject_info.delete()
                    return Response({
                        'result': 'success',
                        "output": "Subject deleted successfully"
                    }, status=status.HTTP_200_OK)
                else:
                    subject_info.is_archived = True
                    subject_info.save()
                    return Response({
                        'result': 'success',
                        "output": "Subject Archived successfully"
                    }, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid Subject information found'}, status=status.HTTP_400_BAD_REQUEST)
