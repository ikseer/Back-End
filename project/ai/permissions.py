

from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is part of the conversation
        # return request.user in obj.users.all()
        print("hhh")
        print(request.user)
        return request.user.user_type == "doctor"
