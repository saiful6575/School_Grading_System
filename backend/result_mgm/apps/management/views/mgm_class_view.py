from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from ..models.mgm_class import MgmClass
from result_mgm.apps.management.serializers.mgm_class import MgmClassSerializer
from result_mgm.apps.authentication.models.users import User
# Create your views here.


class MgmClassAPI(ModelViewSet):

    lookup_field = 'id'
    queryset = MgmClass.objects.all()
    serializer_class = MgmClassSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.user and request.user.is_superuser:
            return Response({'status': True, 'output': MgmClassSerializer(MgmClass.objects.all(),many=True).data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None):
        try:
            if request.user and request.user.is_superuser:
                return Response({'status': True, 'output': MgmClassSerializer(MgmClass.objects.get(id=id),many=False).data}, status=status.HTTP_200_OK)
            return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid Class information found'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                user = request.data.get('class', {})
                get_staff = MgmClass.objects.get(id=id, is_archived=False)
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
            return Response({'status': False, 'output': 'No Valid Class information found'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            if request.user and request.user.is_superuser:
                user = request.data.get('class', {})
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
            return Response({'status': False, 'output': 'No Valid Class information found'}, status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['put'],
            detail=True,
            url_path='manage-pupil',
            url_name='manage-pupil')
    def manage_pupil(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                class_data = request.data.get('class', {})
                pupil_info = User.objects.get(id=class_data['student_id'],is_student=True)
                get_class = MgmClass.objects.get(id=id, is_archived=False)
                if class_data['action'] == 'ADD':
                    get_class.assigned_pupil.add(pupil_info)
                else:
                    get_class.assigned_pupil.remove(pupil_info)
                return Response({
                    'result': 'success',
                    "output": self.serializer_class(get_class).data
                }, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid Class information found'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                get_class = MgmClass.objects.get(id=id)
                if not get_class.is_archived and get_class.mgm_class_subject_ids.count() <=0:
                    get_class.delete()
                    return Response({
                        'result': 'success',
                        "output": "Class deleted successfully"
                    }, status=status.HTTP_200_OK)
                else:
                    get_class.is_archived = True
                    get_class.save()
                    return Response({
                        'result': 'success',
                        "output": "Class Archived successfully"
                    }, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid Class information found'}, status=status.HTTP_400_BAD_REQUEST)
