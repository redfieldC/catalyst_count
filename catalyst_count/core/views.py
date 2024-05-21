from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import FileUpload,CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import HttpResponse, HttpResponseNotAllowed



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            try:
                user = CustomUser.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('file_list')
            except IntegrityError:
                error_message = "A user with that username already exists."
            except Exception as e:
                error_message = f"An error occurred: {e}"
        else:
            error_message = "Username and password are required."
        return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('file_list')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


def file_list(request):
    if request.user.is_authenticated:
      files = FileUpload.objects.filter(user=request.user)
      return render(request, 'file_list.html', {'files': files})
    else:
        return render(request,'login.html')

def file_upload(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        FileUpload.objects.create(user=request.user, file=file)
        return redirect('file_list')
    return HttpResponseNotAllowed(['POST'])

def file_delete(request, pk):
    file = get_object_or_404(FileUpload, pk=pk, user=request.user)
    if request.method == 'POST':
        file.delete()
        return redirect('file_list')
    return HttpResponseNotAllowed(['POST'])



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_file_list(request):
    files = FileUpload.objects.filter(user=request.user)
    serializer = FileUploadSerializer(files, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_file_upload(request):
    if 'file' in request.FILES:
        file = request.FILES['file']
        file_upload = FileUpload.objects.create(user=request.user, file=file)
        serializer = FileUploadSerializer(file_upload)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'File not provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_file_delete(request, pk):
    file = get_object_or_404(FileUpload, pk=pk, user=request.user)
    file.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)