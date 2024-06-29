
from .user import *


class Doctor(Profile):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    location = models.CharField(max_length=255,null=True,blank=True)
    price_for_reservation=models.IntegerField(null=True,blank=True)
    approved = models.BooleanField(default=False)


    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def is_doctor():
        return True
