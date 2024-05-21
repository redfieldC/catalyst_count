# myapp/serializers.py
from rest_framework import serializers
from .models import CustomUser, FileUpload



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'firstname', 'lastname', 'email']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'user', 'file', 'uploaded_at']
