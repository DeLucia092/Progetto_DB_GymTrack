from django.shortcuts import render, redirect
from FitStats.models import *
from django.conf import settings
import os
import hashlib
from .forms import IntegratoreForm
import re
from django.utils import timezone
from django.core.cache import cache
# Create your views here.
def index(request):
    return render (request, 'homepage.html', {})

def authenticated(email, password):
    return Utente.objects.filter(email=email, password=password).exists()

def password_sicura(password):
    if len(password) < 8:
        return False, "La password deve essere lunga almeno 8 caratteri."
    if not re.search(r'[A-Z]', password):
        return False, "La password deve contenere almeno una lettera maiuscola."
    if not re.search(r'[a-z]', password):
        return False, "La password deve contenere almeno una lettera minuscola."
    if not re.search(r'\d', password):
        return False, "La password deve contenere almeno un numero."
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return False, "La password deve contenere almeno un carattere speciale."
    return True, ""


def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        if not email or not password:
            return render(request, 'index.html', {'error_message': "Compila tutti i campi"})

        # Recupera tentativi e blocco dalla cache
        failed_attempts = cache.get(f'failed_{email}', 0)
        block_until = cache.get(f'block_{email}')

        now = timezone.now()
        if block_until and now < block_until:
            return render(request, 'index.html', {
                'error_message': "Troppi tentativi falliti. Riprova tra 2 minuti."
            })

        hashed_pass = hashlib.sha256(password.encode()).hexdigest()
        if authenticated(email, hashed_pass):
            cache.delete(f'failed_{email}')
            cache.delete(f'block_{email}')
            utente = Utente.objects.get(email=email)
            request.session['user_email'] = utente.email
            request.session['username'] = utente.username
            if email.lower().endswith('@pt.com'):
                return render(request, 'creazione_schede.html', {'username': utente.username})
            return redirect('mie_schede')
        else:
            failed_attempts += 1
            cache.set(f'failed_{email}', failed_attempts, timeout=120)
            if failed_attempts >= 3:
                block_time = now + timezone.timedelta(minutes=2)
                cache.set(f'block_{email}', block_time, timeout=120)
                cache.set(f'failed_{email}', 0, timeout=120)
                return render(request, 'index.html', {
                    'error_message': "Troppi tentativi falliti. Riprova tra 2 minuti."
                })
            return render(request, 'index.html', {'error_message': "Credenziali non valide, riprova"})
    else:
        return render(request, 'index.html', {'error_message': "Metodo non valido"})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        if not username or not password or not email:
            return render(request, 'registration.html', {'error_message': "Compila tutti i campi"})
        ok, msg = password_sicura(password)
        if not ok:
            return render(request, 'registration.html', {'error_message': msg})
        return registration_function(email, username, password, request)
    else:
        return render(request, 'registration.html')

def registration_function(email, username, password, request):
    if Utente.objects.filter(email=username).exists():
        return render(request, 'registration.html', {'error_message': "Utente esiste già"})
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
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
        ok, msg = password_sicura(password)
        if not ok:
            return render(request, 'registrazione_cliente.html', {'error_message': msg})
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
        ok, msg = password_sicura(password)
        if not ok:
            return render(request, 'registrazione_trainer.html', {'error_message': msg})
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
    username = request.session.get('username', '')
    if not username:
        return redirect('login')

    esercizi = Esercizio.objects.all()
    success_message = None
    error_message = None

    if request.method == 'POST':
        giorno_inizio = request.POST.get('giorno_inizio')
        giorno_fine = request.POST.get('giorno_fine')
        email_utente = request.POST.get('email_utente')
        nomi_giornata = request.POST.getlist('nomi_giornata[]')

        try:
            utente = Utente.objects.get(email=email_utente)
            # Crea la scheda UNA SOLA VOLTA
            scheda = Scheda.objects.create(
                giorno_inizio=giorno_inizio,
                giorno_fine=giorno_fine,
                email_utente=utente,
                creata_da=username
            )

            for idx, nome_giornata in enumerate(nomi_giornata):
                esercizi_ids = request.POST.getlist(f'esercizi_{idx}[]')
                serie_list = request.POST.getlist(f'serie_PT_{idx}[]')
                ripetizioni_list = request.POST.getlist(f'ripetizioni_{idx}[]')
                recupero_list = request.POST.getlist(f'tempo_recupero_{idx}[]')

                if not (esercizi_ids and serie_list and ripetizioni_list and recupero_list):
                    error_message = "Compila tutti i parametri per ogni esercizio."
                    break

                for e_idx, esercizio_id in enumerate(esercizi_ids):
                    esercizio = Esercizio.objects.get(pk=esercizio_id)
                    Composizione.objects.create(
                        nome_giornata=nome_giornata,
                        nome_esercizio=esercizio,
                        scheda=scheda,
                        serie_PT=serie_list[e_idx],
                        ripetizioni=ripetizioni_list[e_idx],
                        tempo_recupero=recupero_list[e_idx]
                    )
            if not error_message:
                success_message = "Scheda creata con successo!"
        except Exception as e:
            error_message = "Errore nella creazione della scheda: " + str(e)

    return render(request, 'pagina_creazione_scheda.html', {
        'esercizi': esercizi,
        'success_message': success_message,
        'error_message': error_message
    })

def mie_schede(request):
    username = request.session.get('username')
    user_email = request.session.get('user_email')
    if not username or not user_email:
        return redirect('login')

    # Recupera tutte le schede dell'utente
    schede = Scheda.objects.filter(
        id_scheda__in=Composizione.objects.filter(
            scheda__email_utente__email=user_email
        ).values_list('scheda__id_scheda', flat=True)
    ).distinct()

    scheda_selezionata = None
    esercizi = None
    if request.method == 'POST':
        scheda_id = request.POST.get('scheda_id')
        if scheda_id:
            scheda_selezionata = schede.filter(id_scheda=scheda_id).first()
            # Recupera tutte le composizioni (esercizi) della scheda selezionata
            esercizi = Composizione.objects.filter(scheda__id_scheda=scheda_id)

    return render(request, 'mie_schede.html', {
        'username': username,
        'schede': schede,
        'scheda_selezionata': scheda_selezionata,
        'esercizi': esercizi  # Ogni esercizio ha esercizio.nome_giornata
    })


def aggiungi_integratore(request):
    if request.method == 'POST':
        form = IntegratoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mie_schede')
    else:
        form = IntegratoreForm()
    return render(request, 'aggiungi_integratore.html', {'form': form})


import sqlite3

# def authenticated_vulnerabile(email, password):
#     conn = sqlite3.connect('db.sqlite3')
#     cursor = conn.cursor()
#
#     query = f"SELECT * FROM Utente WHERE email = '{email}' AND password = '{password}'"
#     cursor.execute(query)
#     result = cursor.fetchone()
#
#     conn.close()
#     return result is not None

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.form['email']
#     password = request.form['password']
#     if authenticated_vulnerabile(email, password):
#         return "Login Success"
#     else:
#         return "Invalid credentials"

