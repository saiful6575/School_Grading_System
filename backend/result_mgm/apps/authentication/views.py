from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models.users import User
from .serializers.users import RegistrationUserSerializer,LoginSerializer
# Create your views here.


class UserAPI(ModelViewSet):
    """
           Users API endpoint
           Users List : /api/users/datatable
           Users List in Scheduler: /api/users/scheduler
           Users List for all : /api/users/generic
    """
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = RegistrationUserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.user and request.user.is_superuser:
            return Response({'status': True, 'output': RegistrationUserSerializer(User.objects.all(),many=True).data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None):
        try:
            if request.user and request.user.is_superuser:
                return Response({'status': True, 'output': RegistrationUserSerializer(User.objects.get(id=id),many=False).data}, status=status.HTTP_200_OK)
            return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid User information found'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                user = request.data.get('user', {})
                get_staff = User.objects.get(id=id)
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
        print(request.user)
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'result': 'success',
                "output": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'result': 'error',
                'output': {},
                'message': serializer.errors,

            }, status=status.HTTP_200_OK)



class LoginUserAPI(APIView):
    """
           Users API endpoint
           Users List : /api/users/datatable
           Users List in Scheduler: /api/users/scheduler
           Users List for all : /api/users/generic
    """
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            return Response({
                'result': 'success',
                'output': serializer.data,
                'message': ''
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'result': 'error',
                'output': {},
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)