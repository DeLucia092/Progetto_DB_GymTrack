from django.shortcuts import render
from FitStats.models import User

import hashlib
# Create your views here.
def index(request):
    return render (request, 'index.html', {})

def authenticated(email, password):
    return User.objects.filter(email=email, password=password).exists()

def login(request):
    if request.method == 'POST':
        email=request.POST.get('username')
        password= request.POST.get('password')
        hashed_pass=hashlib.md5(password.encode()).hexdigest()

        if (authenticated(email, hashed_pass)):
            return render(request, 'homepage.html', {'username': email})
        else:
            return render(request, 'index.html', {'error_message': "Credenziali non valide, riprova"})
    else:
        return render(request, 'index.html', {'error_message': "Metodo non valido"})

def register(request):
    username=request.POST.get('username')
    password= request.POST.get('password')
    registration_function(username, password, request)
    return render(request, 'index.html', {'username': username})

def registration_function(username,password, request):
    if (User.objects.filter(email=username).exists()):
        return render(request, 'registration.html', {'error_message': "utente esiste già"})
    else:
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        user = User(email=username, password=hashed_password)
        user.save()
        return render(request, 'index.html', {})

