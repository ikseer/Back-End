from django.contrib import admin
from django.urls import include, path

from accounts.views import *
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    ### profile ###
    path('', include(router.urls)),
    # path('api/token/', CustomTokenObtainPairView.as_view(), name='rest_login'),
    path('login/', CustomTokenObtainPairView.as_view(), name='rest_login'),


    ### Usre ###
    path('otp-by-email/', OtpByEmailView.as_view(), name='otp-by-email'),

    path('verify-email-otp/', VerifyEmailOtpView.as_view(), name='verify-email-otp'),


    ### phone ###
    path("phone/<phone>/", getPhoneNumberRegistered_TimeBased.as_view(), name="OTP_Gen"),

    ### social  ###
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    ### dj-rest-auth ###
    
    path('', include('dj_rest_auth.urls')),
    path('register/', CustomRegisterView.as_view(), name='rest_register'),
    path('rest-auth/password/reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    
    ### allauth ###
    path('allauth/', include('allauth.urls')),

]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
