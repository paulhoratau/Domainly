
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .models import Domain
from .serializers import UserSerializer, DomainSerializer, DomainSearchSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

class DomainCreate(generics.CreateAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




class DomainDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer


class DomainSearch(APIView):
    def get(self, request):
        domain = request.GET.get("domain")
        queryset = Domain.objects.filter(domain=domain).exists()
        response = {"exists": queryset}
        return Response(response)
