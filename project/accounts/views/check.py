from .views import *


# check if password of user is correct
class CheckPasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = CheckPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]
        user = request.user
        if user.check_password(password):
            return Response({"password_correct":True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"password_correct":False}, status=status.HTTP_400_BAD_REQUEST
            )





class CheckEmailView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = CheckEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        email_address = EmailAddress.objects.filter(email=email, verified=True).first()
        if email_address:
            return Response({"email_exists": True}, status=status.HTTP_200_OK)
        else:
            return Response({"email_exists": False}, status=status.HTTP_200_OK)


class CheckUsernameView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckUsernameSerializer

    def post(self, request, *args, **kwargs):
        serializer = CheckUsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        user = User.objects.filter(username=username).first()
        if user:
            return Response({"username_exists": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"username_exists": False}, status=status.HTTP_200_OK
            )
