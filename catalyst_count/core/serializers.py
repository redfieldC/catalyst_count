# myapp/serializers.py
from rest_framework import serializers
from .models import CustomUser, Company



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'firstname', 'lastname', 'email']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
