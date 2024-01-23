import email
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from accounts.serializers import *
from .utils import *
from rest_framework import status
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
import base64
from dj_rest_auth.registration.views import RegisterView
from rest_framework import viewsets , generics
from rest_framework.generics import GenericAPIView
from .models import *
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.decorators import api_view, permission_classes
from .utils import *
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import LoginView
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# check if email exists and verified 
class CheckEmailView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckEmailSerializer
    def post(self, request, *args, **kwargs):
        serializer = CheckEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        email_address = EmailAddress.objects.filter(email=email, verified=True).first()
        if email_address:
            return Response({'email_exists': True}, status=status.HTTP_200_OK)
        else:
            return Response({'email_exists': False}, status=status.HTTP_404_NOT_FOUND)
class CheckUsernameView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckUsernameSerializer
    def post(self, request, *args, **kwargs):
        serializer = CheckUsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.filter(username=username).first()
        if user:
            return Response({'username_exists': True}, status=status.HTTP_200_OK)
        else:
            return Response({'username_exists': False}, status=status.HTTP_404_NOT_FOUND)
class CustomTokenObtainPairView(LoginView):
    pass

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]



    

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegistration
    # permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:    
            user=User.objects.filter(email=self.request.data['email']).last()
            SendEmail.send_otp(user)
            # save to profile
            # profile = Profile.objects.get(user=user)
            # profile.gender = self.request.data['gender']
            # profile.save()
        return Response({'detail': 'Verify your email' }, status=status.HTTP_201_CREATED)
    


class OtpByEmailView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OtpByEmailSerializer
    def post(self, request, *args, **kwargs):
        serializer = OtpByEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "Invalid Email"}, status=status.HTTP_400_BAD_REQUEST)

            SendEmail.send_otp(user)
            return Response({"detail": "OTP sent to your email"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VerifyEmailOtpView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailOtpSerializer
    def post(self, request, *args, **kwargs):
        serializer = VerifyEmailOtpSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']

            user = Otp.verify_otp(otp)
            if not user:
                return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserDetailsSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    # callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
    client_class = OAuth2Client

class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


# Time after which OTP will expire
EXPIRY_TIME = 120 # seconds

class getPhoneNumberRegistered_TimeBased(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = PhoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            PhoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = PhoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model for OTP is created
        # send_otp_via_email(request, OTP.now())
        response_data = {
            "message": "OTP  sent to the mobile number ",
            "OTP": OTP.now(),
        }

        return Response(response_data, status=status.HTTP_200_OK)

#     # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = PhoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model 
        if OTP.verify(request.data["otp"]):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.user=request.user
            Mobile.save()
            return Response("You are authorised", status=200)
            
        return Response("OTP is wrong/expired", status=400)