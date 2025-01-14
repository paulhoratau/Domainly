
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .models import Domain
from .serializers import UserSerializer, DomainSerializer, DomainSearchSerializer, WhoisSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import whois
from rest_framework import status
import subprocess

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



class WhoisLookupView(APIView):
    def post(self, request):
        serializer = WhoisSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data['domain']
            try:
                domain_info = subprocess.check_output(["whois", domain])
                output = {"output": domain_info}
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(output, status=status.HTTP_200_OK)
