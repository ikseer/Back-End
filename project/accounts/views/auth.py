

from .views import *


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegistration

    # permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer=CustomRegistration(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        response  = super().post(request, *args, **kwargs)
        user = User.objects.get(id=response.data['user']['pk'])

        if 'user_type' in serializer.data:
            user.user_type=serializer.data['user_type']
            user.save()

        POSITIONS[user.user_type].objects.create(
            user=user,
            first_name=serializer.data['first_name'],
            last_name = serializer["last_name"]   ,
            gender = serializer["gender"] )



        SendEmail.send_otp(user)
        return Response({"detail": "Verify your email"}, status=status.HTTP_201_CREATED)


# check if email exists and verified
class UnlinkProviderView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UnlinkProviderSerializer

    def post(self, request, *args, **kwargs):
        serializer = UnlinkProviderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data["provider"]
        user = User.objects.get(email=serializer.validated_data["email"])
        social_account = SocialAccount.objects.get(user=user, provider=provider)

        if social_account:
            # send unlink to provider

            social_account.delete()
            signals.social_account_removed.send(
                sender=SocialAccount, request=self.request, socialaccount=social_account
            )
            return Response(
                {"detail": "Provider unlinked successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Provider not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CustomTokenObtainPairView(LoginView):
    pass


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(
    SocialLoginView
):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    # callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
    client_class = OAuth2Client
