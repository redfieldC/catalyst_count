from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import FileUpload,CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError



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
