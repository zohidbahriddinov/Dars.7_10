from .models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone']
        read_only_fields = ['is_admin', 'is_staff', 'is_active']


class DaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'

class RoomsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'

class TebleTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = '__all__'

class TableSerializers(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class GroupStudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': "Login yoki parol noto'g'ri."})

        if not user.check_password(password):
            raise serializers.ValidationError({'detail': "Login yoki parol noto'g'ri."})

        if not user.is_active:
            raise serializers.ValidationError({'detail': "Foydalanuvchi aktiv emas."})

        attrs['user'] = user
        return attrs

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()    


class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['id', 'title', 'descriptions', 'is_active', 'created_ed', 'updated_ed']


class CouresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coures
        fields = ['id', 'title', 'descriptions', 'created_ed', 'updated_ed']


class TecherSerializer(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Techer
        fields = '__all__'

    def create(self, validated_data):
        user_db = validated_data.pop('user')
        departments_db = validated_data.pop('departmenst', [])
        course_db = validated_data.pop('coures', [])

        raw_password = user_db.pop('password')
        user_db['is_active'] = False
        user_db['is_teacher'] = True

        user = User(**user_db)
        user.set_password(raw_password)
        user.save()

        techer = Techer.objects.create(user=user, **validated_data)
        techer.departmenst.set(departments_db)
        techer.coures.set(course_db)

        return techer



class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Student
        fields = ['user', 'is_line', 'descriptions']

    def create(self, validated_data):
        user_db = validated_data.pop('user')

        raw_password = user_db.pop('password')
        user_db['is_active'] = False
        user_db['is_student'] = True

        user = User(**user_db)
        user.set_password(raw_password)
        user.save()

        student = Student.objects.create(
            user=user,
            is_line=validated_data.get('is_line', False),
            descriptions=validated_data.get('descriptions', "")
        )

        return student

    
class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError({'email': 'Bunday email mavjud emas.'})

        attrs['user_instance'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user_instance']
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.is_active = True
        user.save()
        return user
