from rest_framework import serializers
from django.contrib.auth import get_user_model  # If using a custom user model
from .models import Domain, Transaction
from .validators import validate_domain
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only
    def create(self, validated_data):
        # Create user with hashed password
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password")

class DomainSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    card_number = serializers.CharField(write_only=True) 
    date = serializers.CharField(write_only=True)
    cvv = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = Domain
        fields = ['domain', 'owner', 'valid_from', 'expires_at', 'card_number', 'date', 'cvv', 'full_name']

    def create(self, validated_data):
        card_number = validated_data.pop('card_number')
        date = validated_data.pop('date')
        cvv = validated_data.pop('cvv')
        full_name = validated_data.pop('full_name')
        domain = Domain.objects.create(**validated_data)
        Transaction.objects.create(
            domain=domain,
            card_last4=card_number[-4:],
            date=date,
            cvv=cvv,
            full_name=full_name
        )

        return domain

class DomainSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain']

class WhoisSerializer(serializers.Serializer):
    domain = serializers.CharField(max_length=255)

class UserDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["domain", "valid_from", "expires_at"]
