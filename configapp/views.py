from django.shortcuts import render,get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import viewsets, permissions
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .make_token import *

class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class DayModelViewSet(ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializers

class RoomsModelViewSet(ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializers

class TebleTypeModelViewSet(ModelViewSet):
    queryset = TableType.objects.all()
    serializer_class = TebleTypeSerializers

class TableModelViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializers

class GroupStudentModelViewSet(ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializers

class DepartmentsModelViewSet(ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer

class CouresModelViewSet(ModelViewSet):
    queryset = Coures.objects.all()
    serializer_class = CouresSerializer



class StudentAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()

            password = request.data['user']['password']
            email = request.data['user']['email']

            subject = 'Sizning login malumotlaringiz'
            message = f"Siz tizimga quyidagi ma'lumotlar bilan kirishingiz mumkin:\nEmail: {email}\nParol: {password}"

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, email_from, recipient_list)
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TecherAPIView(APIView):
    def get(self, request):
        techers = Techer.objects.all()
        serializer = TecherSerializer(techers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TecherSerializer)
    def post(self, request):
        serializer = TecherSerializer(data=request.data)
        if serializer.is_valid():
            techer = serializer.save()

            password = request.data['user']['password']
            email = request.data['user']['email']

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            subject = 'Sizning login malumotlaringiz'
            message = f"Siz tizimga quyidagi ma'lumotlar bilan kirishingiz mumkin:\nEmail: {email}\nParol: {password}"

            send_mail(subject, message, email_from, recipient_list)

            return Response(TecherSerializer(techer).data, status=201)
        return Response(serializer.errors, status=400)


class LoginUser(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer, responses={200: TokenSerializer()})
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = get_object_or_404(User, username=username)

        if not user.check_password(password):
            return Response({'detail': 'Noto\'g\'ri parol.'}, status=400)
        
        tokens = get_tokens_for_user(user)


        token_serializer = TokenSerializer(data=tokens)
        token_serializer.is_valid(raise_exception=True)

        return Response(token_serializer.data, status=200)
    

class UpdatePasswordAPIView(APIView):
    @swagger_auto_schema(request_body=UpdatePasswordSerializer)

    def post(self ,request):
        serializers = UpdatePasswordSerializer(data = request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(
                {
                    'success' : True,
                    'massage' : "Parol muvaffaqiyatli yangilandi."
                },
                status=status.HTTP_200_OK
            )
        return Response(serializers.errors , status=status.HTTP_400_BAD_REQUEST)
    

