from rest_framework import serializers
from django.contrib.auth import get_user_model  # If using a custom user model
from .models import Domain
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
        fields = ("id", "username", "password", )

class DomainSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(validators=[validate_domain, UniqueValidator(queryset=Domain.objects.all())])
    owner = serializers.ReadOnlyField(source='owner.username')
    card_number = serializers.CharField(min_length=16, max_length=16, validators=[RegexValidator(regex=r'^\d+$', message="Only numbers allowed.")])
    date = serializers.CharField(min_length=5, max_length=5, validators=[RegexValidator(regex=r'^[\d/]+$', message="Only numbers and '/' allowed.")])
    cvv = serializers.CharField(min_length=3, max_length=3, validators=[RegexValidator(regex=r'^\d+$', message="Only numbers allowed.")])
    full_name = serializers.CharField(max_length=30, validators=[RegexValidator(regex=r'^[A-Za-z]+$', message="Only letters allowed.")])
    class Meta:
        model = Domain
        fields = '__all__'

    def to_representation(self, instance):
        return {"message": getattr(self, "success_message", "Your domain has been successfully bought!")}

class DomainSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain']
