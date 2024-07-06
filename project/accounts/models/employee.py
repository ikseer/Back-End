
from .user import *


class Employee(Profile):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)


    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def is_employee():
        return True
