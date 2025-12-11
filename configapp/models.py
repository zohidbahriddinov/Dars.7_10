from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="+998XXXXXXXXX formatida kiriting."
    )

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.is_admin

class BaseModel(models.Model):
    created_ed = models.DateField(auto_now_add=True)
    updated_ed = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Day(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Rooms(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class TableType(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Coures(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Departments(BaseModel):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

class Techer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    departmenst = models.ManyToManyField(Departments, related_name='teachers')
    coures = models.ManyToManyField(Coures, related_name='teachers')
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.email


class Table(BaseModel):
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(Rooms, on_delete=models.RESTRICT)
    type = models.ForeignKey(TableType, on_delete=models.RESTRICT)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.start_time.__str__()+"  "+self.end_time.__str__()

class GroupStudent(BaseModel):
    title = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey(Coures, on_delete=models.RESTRICT, related_name="groups")
    teacher = models.ManyToManyField(Techer, related_name='groups')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    is_line = models.BooleanField(default=False)
    descriptions = models.CharField(max_length=500 , blank=True , null=True)

    def __str__(self):
        return self.user.email
