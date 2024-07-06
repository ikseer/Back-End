# -*- coding: utf-8 -*-
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LogoutView, PasswordChangeView, UserDetailsView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import *

router = DefaultRouter()
router.register(r"patient", PatientViewSet, basename="patient")
router.register(r"doctor", DoctorViewSet, basename="doctor")
router.register(r"employee", DoctorViewSet, basename="employee")

router.register(r'users', CustomUserViewSet)
router.register(r'phone', PhoneViewSet)
router.register(r'group', GroupViewSet)
router.register(r'permission', PermissionViewSet)

urlpatterns = [
    ### profile ###
    path("login/", CustomTokenObtainPairView.as_view(), name="rest_login"),
    ### User ###
    path("check-email/", CheckEmailView.as_view(), name="check-email"),
    path("check-username/", CheckUsernameView.as_view(), name="check-username"),
    path("check-password/", CheckPasswordView.as_view(), name="check-password"),
    path("otp-by-email/", OtpByEmailView.as_view(), name="otp-by-email"),
    path("verify-email-otp/", VerifyEmailOtpView.as_view(), name="verify-email-otp"),
    ### phone ###
    path("phone-register/", PhoneRegister.as_view(), name="phone-register"),
    path("verify-mobile-otp/", VerifyMobileOTP.as_view(), name="verify-mobile-otp"),
    ### social  ###
    path("dj-rest-auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("dj-rest-auth/google/", GoogleLogin.as_view(), name="google_login"),

    path("register/", CustomRegisterView.as_view(), name="rest_register"),

    path('statistics/', Statistics.as_view({'get': 'get'}), name='dashboard'),

]

urlpatterns += [
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
]

urlpatterns+=[

    # path('patient/deleted/', PatientViewSet.as_view({'get': 'get_deleted'}), name='patient-get-deleted'),
    # path('doctor/deleted/', DoctorViewSet.as_view({'get': 'get_deleted'}), name='doctor-get-deleted'),

    # path('deleted-patient/restore/<str:pk>/', DeletedPatientView.as_view({'post': 'restore'}), name='patient-restore'),
    # path('deleted-patient/delete/<str:pk>/', DeletedPatientView.as_view({'delete': 'destroy'}), name='deleted-patient-delete'),

    # path('deleted-doctor/restore/<str:pk>/', DeletedDoctorView.as_view({'post': 'restore'}), name='doctor-restore'),
    # path('deleted-doctor/delete/<str:pk>/', DeletedDoctorView.as_view({'delete': 'destroy'}), name='deleted-doctor-delete'),

]
urlpatterns+=[
        path("", include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
