

from .user import *


class EmailVerificationOTP(BaseModel):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.IntegerField(null=True, blank=True)
    activation_key = models.CharField(max_length=150, blank=True, null=True)
