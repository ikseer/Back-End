
from .user import *


class Patient(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def is_patient():
        return True
