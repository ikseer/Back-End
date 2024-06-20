# Create your views here.
# myapp/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Conservation, Message
from .serializers import ConservationSerializer, MessageSerializer


class ConservationViewSet(viewsets.ModelViewSet):
    queryset = Conservation.objects.all()
    serializer_class = ConservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conservation = serializer.save()
        # conservation.users.add(self.request.user)
        conservation.users.set([self.request.user])

        conservation.save()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
