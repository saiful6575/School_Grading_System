from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from ..models.mgm_test import MgmTest
from result_mgm.apps.management.serializers.mgm_test import MgmTestSerializer
# Create your views here.


class MgmTestAPI(ModelViewSet):

    lookup_field = 'id'
    queryset = MgmTest.objects.all()
    serializer_class = MgmTestSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.user and request.user.is_superuser:
            return Response({'status': True, 'output': MgmTestSerializer(MgmTest.objects.all(),many=True).data}, status=status.HTTP_200_OK)
        elif request.user and request.user.is_teacher:
            return Response({'status': True, 'output': MgmTestSerializer(MgmTest.objects.filter(subject_id__assigned_teacher__id=request.user.id),many=True).data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None):
        try:
            if request.user and request.user.is_superuser:
                return Response({'status': True, 'output': MgmTestSerializer(MgmTest.objects.get(id=id),many=False).data}, status=status.HTTP_200_OK)
            elif request.user and request.user.is_teacher:
                return Response({'status': True, 'output': MgmTestSerializer(MgmTest.objects.get(id=id, subject_id__assigned_teacher__id=request.user.id),many=False).data}, status=status.HTTP_200_OK)
            return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid test information found'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                test = request.data.get('test', {})
                get_staff = MgmTest.objects.get(id=id)
                serializer = self.serializer_class(get_staff, data=test, partial=True)
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
                test = request.data.get('test', {})
                serializer = self.serializer_class(data=test)
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
