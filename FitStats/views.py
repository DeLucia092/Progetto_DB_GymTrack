from django.shortcuts import render, redirect
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
            user = User.objects.get(email=email)
            request.session['user_email'] = user.email  # Salva l'email dell'utente nella sessione
            request.session['username'] = user.username  # Salva lo username reale
            return redirect('homepage')
        else:
            return render(request, 'index.html', {'error_message': "Credenziali non valide, riprova"})
    else:
        return render(request, 'index.html', {'error_message': "Metodo non valido"})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        if not username or not password:
            return render(request, 'registration.html', {'error_message': "Compila tutti i campi"})
        return registration_function(email, username, password, request)
    else:
        return render(request, 'registration.html')

def registration_function(email, username, password, request):
    if User.objects.filter(email=username).exists():
        return render(request, 'registration.html', {'error_message': "Utente esiste già"})
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    user = User(email=email, password=hashed_password, username=username)
    user.save()
    return render(request, 'index.html', {'username': username})

def homepage(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    return render(request, 'homepage.html', {'username': username})

def logout(request):
    request.session.flush()
    return redirect('login')  # Assicurati che 'login' sia il nome della tua url di login