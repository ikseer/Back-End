

from rest_framework.permissions import BasePermission


class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is part of the conversation
        # return request.user in obj.users.all()

        return request.user == obj.patient.user or  request.user == obj.doctor.user

class IsParticipantInConversation(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is part of the conversation associated with the message
        return request.user in obj.conversation.users.all()
#
