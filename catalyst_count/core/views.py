from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Company,CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes
from django.http import HttpResponse, HttpResponseNotAllowed
from django.middleware.csrf import get_token
import csv
from io import TextIOWrapper,BytesIO
import chardet
import os 



def all_users(request):
    all_users = CustomUser.objects.all()
    data = {"users":all_users}
    return render(request,'all_users.html',context=data)


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
      files = Company.objects.filter(user=request.user)
      return render(request, 'file_list.html', {'files': files})
    else:
        return render(request,'login.html')

def file_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        
        # Check if the file is a CSV
        if not file.name.endswith('.csv'):
            return HttpResponseNotAllowed(['POST'])

        # Define a temporary file path on the U drive
        upload_dir = 'U:/django/catalyst_count/media/uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        destination = os.path.join(upload_dir, file.name)

        # Write the uploaded file to the destination file
        with open(destination, 'wb+') as destination_file:
            for chunk in file.chunks():
                destination_file.write(chunk)

        # Process the uploaded CSV file
        with open(destination, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Extract data from each row and create a new Company instance
                locality = row.get('locality', '')
                if locality:
                    city_state = locality.split(',')[:2]
                    city = city_state[0].strip() if len(city_state) > 0 else 'Unknown'
                    state = city_state[1].strip() if len(city_state) > 1 else 'Unknown'
                else:
                    city = 'Unknown'
                    state = 'Unknown'

                # Convert year founded to integer
                try:
                    year_founded = int(float(row.get('year founded', 0)))
                except ValueError:
                    year_founded = 2021  # default year if conversion fails  
                
                Company.objects.create(
                    user=request.user,
                     name=row.get('name', 'Unknown'),
                    domain=row.get('domain', 'Unknown'),
                    year=year_founded,
                    industry=row.get('industry', 'UNKNOWN'),
                    size_range=row.get('size range', 'Unknown'),
                    city=city,
                    state=state,
                    country=row.get('country', 'Unknown'),
                    linkedin_url=row.get('linkedin url', 'Unknown'),
                    current_employee_estimate=row.get('current employee estimate'),
                    total_employee_estimate=row.get('total employee estimate')
                )

        # Delete the temporary file after processing
        os.remove(destination)

        # Redirect to file_list after processing
        return redirect('file_list')

    # If request is not POST or file is not present, return method not allowed
    return HttpResponseNotAllowed(['POST'])


def query_builder(request):
        # Get the parameters from the request.POST
        # keyword = request.GET.get('keyword')
        industry = request.GET.get('industry')
        year = request.GET.get('year')
        city = request.GET.get('city')
        state = request.GET.get('state')
        country = request.GET.get('country')
        employees_from = request.GET.get('employees_from')
        employees_to = request.GET.get('employees_to')

        # Start with all companies
        companies = Company.objects.all()

        # Apply filters based on the parameters
        # if keyword:
        #     companies = companies.filter(name__icontains=keyword)
        if industry:
            companies = companies.filter(industry__icontains=industry)
        if year:
            companies = companies.filter(year=year)
        if city:
            companies = companies.filter(city__icontains=city)
        if state:
            companies = companies.filter(state__icontains=state)
        if country:
            companies = companies.filter(country__icontains=country)
        if employees_from:
            companies = companies.filter(employees__gte=employees_from)
        if employees_to:
            companies = companies.filter(employees__lte=employees_to)

        # Render the results
        count = companies.count()
        return render(request, 'query_builder.html',{'count':count})


# def file_delete(request, pk):
#     file = get_object_or_404(Company, pk=pk, user=request.user)
#     if request.method == 'POST':
#         file.delete()
#         return redirect('file_list')
#     return HttpResponseNotAllowed(['POST'])



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def api_file_list(request):
#     files = Company.objects.filter(user=request.user)
#     serializer = CompanySerializer(files, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def api_file_upload(request):
#     if 'file' in request.FILES:
#         file = request.FILES['file']
#         file_upload = Company.objects.create(user=request.user, file=file)
#         serializer = CompanySerializer(file_upload)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response({'error': 'File not provided'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def api_file_delete(request, pk):
#     file = get_object_or_404(Company, pk=pk, user=request.user)
#     file.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')
    email = request.data.get('email')
    
    if username and password and email:
        try:
            user = CustomUser.objects.create_user(
                username=username, 
                password=password, 
                email=email,
                firstname=firstname,
                lastname=lastname
            )
            login(request, user)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'A user with that username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'error': 'Username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_file_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Check if the file is a CSV
        if not file.name.endswith('.csv'):
            return Response({'error': 'File is not a CSV'}, status=status.HTTP_400_BAD_REQUEST)

        # Define a temporary file path on the U drive
        upload_dir = 'U:/django/catalyst_count/media/uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        destination = os.path.join(upload_dir, file.name)

        # Write the uploaded file to the destination file
        with open(destination, 'wb+') as destination_file:
            for chunk in file.chunks():
                destination_file.write(chunk)

        # Process the uploaded CSV file
        try:
            with open(destination, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                companies = []
                for row in reader:
                    # Extract data from each row and create a new Company instance
                    locality = row.get('locality', '')
                    if locality:
                        city_state = locality.split(',')[:2]
                        city = city_state[0].strip() if len(city_state) > 0 else 'Unknown'
                        state = city_state[1].strip() if len(city_state) > 1 else 'Unknown'
                    else:
                        city = 'Unknown'
                        state = 'Unknown'

                    # Convert year founded to integer
                    try:
                        year_founded = int(float(row.get('year founded', 0)))
                    except ValueError:
                        year_founded = 2021  # default year if conversion fails  

                    company_data = {
                        'user': request.user.id,
                        'name': row.get('name', 'Unknown'),
                        'domain': row.get('domain', 'Unknown'),
                        'year': year_founded,
                        'industry': row.get('industry', 'UNKNOWN'),
                        'size_range': row.get('size range', 'Unknown'),
                        'city': city,
                        'state': state,
                        'country': row.get('country', 'Unknown'),
                        'linkedin_url': row.get('linkedin url', 'Unknown'),
                        'current_employee_estimate': row.get('current employee estimate'),
                        'total_employee_estimate': row.get('total employee estimate')
                    }
                    
                    serializer = CompanySerializer(data=company_data)
                    if serializer.is_valid():
                        serializer.save()
                        companies.append(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        finally:
            # Delete the temporary file after processing
            if os.path.exists(destination):
                os.remove(destination)

        # Redirect to file_list after processing
        return Response(companies, status=status.HTTP_201_CREATED)

    # If request is not POST or file is not present, return method not allowed
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_query_builder(request):
    industry = request.GET.get('industry')
    year = request.GET.get('year')
    city = request.GET.get('city')
    state = request.GET.get('state')
    country = request.GET.get('country')
    employees_from = request.GET.get('employees_from')
    employees_to = request.GET.get('employees_to')

    companies = Company.objects.all()

    if industry:
        companies = companies.filter(industry__icontains=industry)
    if year:
        companies = companies.filter(year=year)
    if city:
        companies = companies.filter(city__icontains=city)
    if state:
        companies = companies.filter(state__icontains=state)
    if country:
        companies = companies.filter(country__icontains=country)
    if employees_from:
        companies = companies.filter(current_employee_estimate__gte=employees_from)
    if employees_to:
        companies = companies.filter(current_employee_estimate__lte=employees_to)

    serializer = CompanySerializer(companies, many=True)
    return Response({'count': companies.count(), 'companies': serializer.data}, status=status.HTTP_200_OK)