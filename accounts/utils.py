import pyotp
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail  # Import send_mail
from PIL import Image

from .models import EmailVerificationOTP

User = get_user_model()


def create_image():
    image = Image.new("RGB", (200, 200), color=(255, 255, 255))
    return image


class SendEmail:
    @staticmethod
    def send_otp(user):
        # otp = GenerateKey.returnValue_email()["OTP"]
        value = Otp.returnValue_email()
        otp = value["OTP"]
        key = value["totp"]
        try:
            email_verification = EmailVerificationOTP.objects.get(user=user)
            email_verification.otp = otp
            email_verification.activation_key = key
            email_verification.save()

        except ObjectDoesNotExist:
            email_verification = EmailVerificationOTP.objects.create(
                user=user, otp=otp, activation_key=key
            )
            email_verification.save()

        # Send the OTP
        subject = "Your OTP Code"
        body = f"Your OTP is: {otp}"
        send_mail(subject, body, "your_email@gmail.com", [user.email])


class Otp:
    @staticmethod
    def returnValue_email():
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=86400)
        OTP = totp.now()
        return {"totp": secret, "OTP": OTP}

    @staticmethod
    def verify_otp(otp):
        try:
            email_verification = EmailVerificationOTP.objects.get(otp=otp)
        except ObjectDoesNotExist:
            return None

        # user = email_verification.user
        activation_key = email_verification.activation_key
        totp = pyotp.TOTP(activation_key, interval=86400)

        if not totp.verify(otp):
            return None
        user = email_verification.user
        email_address = EmailAddress.objects.filter(
            user__email=email_verification.user.email
        ).first()
        email_address.verified = True
        email_address.save()
        email_verification.delete()

        return user
