from django.urls import path , include
from configapp.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register(r'user' , UserModelViewSet)
router.register(r'day' , DayModelViewSet)
router.register(r'rooms' , RoomsModelViewSet)
router.register(r'tebletype' , TebleTypeModelViewSet)
router.register(r'table' , TableModelViewSet)
router.register(r'groupstudent' , GroupStudentModelViewSet)
router.register(r'departments' , DepartmentsModelViewSet)
router.register(r'coures' , CouresModelViewSet)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
    path('', include(router.urls)), 
    path("students/", StudentAPIView.as_view()),
    path("techers/", TecherAPIView.as_view()),
    path('api/tokenLogin/', LoginUser.as_view() , name='token_obtain_pair'),
    path("update-password/", UpdatePasswordAPIView.as_view(), name="update-password"),
]