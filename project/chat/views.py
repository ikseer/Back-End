# Create your views here.
# myapp/views.py


from chat.filters import ConversationFilter, MessageFilter
from chat.pagination import CustomPagination
from chat.permissions import IsParticipant, IsParticipantInConversation
from chat.utils import unseen_message
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated,IsParticipant]

    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]

    filterset_class = ConversationFilter
    pagination_class = CustomPagination



    def get_queryset(self):
        user = self.request.user

        if user.is_staff:  # Check if the user is an admin
            return Conversation.objects.all()
        else:
            if user.user_type=='patient':
                return  Conversation.objects.filter(patient__user=user)
            elif user.user_type=='doctor':
                return Conversation.objects.filter(doctor__user=user)




class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated,IsParticipantInConversation]

    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]

    filterset_class = MessageFilter
    pagination_class = CustomPagination



    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Check if the user is an admin
            return Message.objects.all()
        else:
            pass
            if user.user_type=='patient':

                return  Message.objects.filter(conversation__patient__user=self.request.user)
            elif user.user_type=='doctor':
                return Message.objects.filter(conversation__doctor__user=self.request.user)
        # return  Message.objects.all()

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        unseen_message(message)


    @action(detail=False, methods=['get'], url_path='unseen')
    def get_unseen_messages(self, request):
        unseen_messages = Message.objects.filter(
            conversation__users=request.user,
            seen_statuses__user=request.user,
            seen_statuses__seen=False
        )
        serializer = self.get_serializer(unseen_messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='mark-seen')
    def mark_as_seen(self, request, pk=None):
        message = self.get_object()
        seen_status, created = MessageSeenStatus.objects.get_or_create(message=message, user=request.user)
        seen_status.seen = True
        seen_status.save()
        return Response({'status': 'message marked as seen'})


class FCMTokenViewSet(viewsets.ModelViewSet):
    queryset=FCMToken.objects.all()
    serializer_class=FCMTokenSerializer
    permission_classes=[IsAuthenticated]
