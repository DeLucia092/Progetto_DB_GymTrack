from django.shortcuts import render, redirect
from FitStats.models import *
from django.conf import settings
import os
import hashlib
# Create your views here.
def index(request):
    return render (request, 'index.html', {})

def authenticated(email, password):
    return Utente.objects.filter(email=email, password=password).exists()

def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        if not email or not password:
            return render(request, 'index.html', {'error_message': "Compila tutti i campi"})

        hashed_pass = hashlib.md5(password.encode()).hexdigest()

        if authenticated(email, hashed_pass):
            utente = Utente.objects.get(email=email)
            request.session['user_email'] = utente.email
            request.session['username'] = utente.username
            # Controllo se trainer
            if email.lower().endswith('@pt.com'):
                return render(request, 'creazione_schede.html', {'username': utente.username})
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
    if Utente.objects.filter(email=username).exists():
        return render(request, 'registration.html', {'error_message': "Utente esiste già"})
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    utente = Utente(email=email, password=hashed_password, username=username)
    utente.save()
    return render(request, 'index.html', {'username': username})

def homepage(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    return render(request, 'homepage.html', {'username': username})

def logout(request):
    request.session.flush()
    return redirect('login')  # Assicurati che 'login' sia il nome della tua url di login

def scelta_registrazione(request):
    return render(request, 'scelta_registrazione.html')

def registrazione_cliente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password or not email:
            return render(request, 'registrazione_cliente.html', {'error_message': "Compila tutti i campi"})
        return registration_function(email, username, password, request)
    else:
        return render(request, 'registrazione_cliente.html')

def registrazione_trainer(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password or not email:
            return render(request, 'registrazione_trainer.html', {'error_message': "Compila tutti i campi"})
        if not email.lower().endswith('@pt.com'):
            return render(request, 'registrazione_trainer.html', {'error_message': "L'email deve terminare con @PT.com"})
        return registration_function(email, username, password, request)
    else:
        return render(request, 'registrazione_trainer.html')


def creazione_schede(request):
    username = request.session.get('username', '')
    if not username:
        return redirect('login')
    utente = Utente.objects.get(username=username)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'aggiungi_certificazione':
            file = request.FILES.get('certificazione')
            if file:
                certificazioni_dir = os.path.join(settings.MEDIA_ROOT, 'certificazioni')
                os.makedirs(certificazioni_dir, exist_ok=True)
                file_path = os.path.join('certificazioni', file.name)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                with open(full_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                utente.certificazione = file_path
                utente.save()
                request.session['success_message'] = "Certificazione aggiunta con successo!"
            else:
                request.session['error_message'] = "Seleziona una foto valida."
            return redirect('creazione_schede')
        elif action == 'aggiungi_stipendio':
            try:
                stipendio = float(request.POST.get('stipendio'))
                utente.stipendio = stipendio
                utente.save()
                request.session['success_message'] = "Stipendio aggiornato con successo!"
            except (ValueError, TypeError):
                request.session['error_message'] = "Inserisci un valore di stipendio valido."
            return redirect('creazione_schede')
        elif action == 'crea_scheda':
            return redirect('pagina_creazione_scheda')

    success_message = request.session.pop('success_message', None)
    error_message = request.session.pop('error_message', None)

    return render(request, 'creazione_schede.html', {
        'username': username,
        'success_message': success_message,
        'error_message': error_message,
        'utente': utente
    })

def pagina_creazione_scheda(request):
 # Logica per la creazione della scheda, se necessaria
    return render(request, 'pagina_creazione_scheda.html')