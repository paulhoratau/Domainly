
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .models import Domain
from .serializers import UserSerializer, DomainSerializer, DomainSearchSerializer, WhoisSerializer, UserDomainSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import whois
from rest_framework import status
import subprocess
User = get_user_model()
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

class Profile(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return self.request.user

class RegisterDomainAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        serializer = DomainSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(owner=request.user)  # Automatically assign owner
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDomains(generics.ListAPIView):
    queryset = Domain.objects.all()
    serializer_class = UserDomainSerializer
    permission_classes = [IsAuthenticated]


class DomainDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [IsAuthenticated]


class DomainSearch(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        domain = request.GET.get("domain")
        queryset = Domain.objects.filter(domain=domain).exists()
        response = {"exists": queryset}
        return Response(response)



class WhoisLookupView(APIView):
    permission_classes = [IsAuthenticated]
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
