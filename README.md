# GymTrack – Sistema Informativo per Schede di Allenamento
GymTrack è un sistema informativo full-stack progettato per digitalizzare e ottimizzare la gestione delle schede di allenamento in palestre, studi di personal training e centri sportivi. L’obiettivo principale è superare le inefficienze dei metodi cartacei, offrendo una piattaforma web responsiva e sicura per Personal Trainer e Clienti, con accesso rapido e organizzato alle schede di allenamento personalizzate.GymTrack è un sistema informativo full-stack progettato per digitalizzare e ottimizzare la gestione delle schede di allenamento in palestre, studi di personal training e centri sportivi. L’obiettivo principale è superare le inefficienze dei metodi cartacei, offrendo una piattaforma web responsiva e sicura per Personal Trainer e Clienti, con accesso rapido e organizzato alle schede di allenamento personalizzate.

---

## Indice

- [Obbiettivi del Progetto](#obbiettivi-del-progetto) 
- [Modello Entità/Relazione](#modello-entitàrelazione)
- [Funzionalità Principali](#funzionalità-principali)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Installazione](#installazione)
- [Configurazione del Database](#configurazione-del-database)
- [Web Application](#web-application)
- [Licenza](#licenza)
- [Utenti](#utenti)

---

## Obiettivi del Progetto
GymTrack nasce dall’esigenza di:

- Digitalizzare la gestione delle schede di allenamento.

- Consentire ai Personal Trainer di creare, assegnare e gestire schede in modo rapido ed efficiente.

- Offrire ai Clienti un accesso organizzato alle proprie schede, con possibilità di tracking dei progressi e gestione della supplementazione.

- Fornire un sistema sicuro, scalabile e manutenibile, pronto per integrazioni future (notifiche push, wearable, dashboard avanzate).

---

## Modello Entità/Relazione
il modello Entità-Relazione rappresenta le principali entità del sistema e le loro relazioni, consentendo di gestire utenti, esercizi, schede, integratori e le altre entità in gioco. La scelta progettuale unifica le entità figlie in un’unica tabella Utente, garantendo maggiore scalabilità e semplicità di query.
<img width="1522" height="602" alt="Diagramma senza titolo-Pagina-2 drawio" src="https://github.com/user-attachments/assets/dd63932e-4341-4746-97ac-35b71a94b083" />

---

## Funzionalità Principali
Registrazione e Login sicuri (hash SHA256, controllo dominio @pt.com per Personal Trainer).

- Gestione ruoli utenti (Cliente, Personal Trainer).

- Creazione schede di allenamento con interfaccia intuitiva e organizzazione per giornate.

- Visualizzazione schede assegnate.

- Gestione integratori: aggiunta integratori con dosaggi personalizzati.

- Filtri esercizi per gruppo muscolare.

---

## Tecnologie Utilizzate
- Python 3

- **Django** (framework backend, ORM, sessioni)

- **SQLite** (database relazionale)

- **HTML5 / CSS3** (frontend responsivo)

- **Django Templates** (rendering dinamico)

- **SHA256** (hashing password)

- **Git + GitHub** (versionamento del codice)

---

## Installazione
Per eseguire l'applicazione, è necessario:

1. Disporre di **Python** installato nel proprio ambiente.
2. Avere accesso a un server, preferibilmente con phpMyAdmin per una gestione semplificata.
3. Clonare il progetto:
   ```bash
   git clone https://github.com/DeLucia092/Progetto_DB_GymTrack.git
   cd Progetto_DB_GymTrack
4. Creare e attivare un ambiente virtuale:
   ```
   python -m venv venv
   ```
    # Linux/macOS
   ```
    source venv/bin/activate
   ```  
    # Su Windows: 
   In Powershell:
   ```
   .\.venv\Scripts\Activate.ps1
   ```
   In cmd:
   ```
   .\.venv\Scripts\activate.bat
   ```
 6. Installare le dipendenze
    ```
    pip install -r requirements.txt
    ```
    Se non si dispone di un file requirements.txt, si puo procedere con la seguente installazione manuale:
    ```
    pip install django
    ```

---

## Configurazione del Database
GymTrack utilizza SQLite integrato in Django. Per configurarlo, controlla il file settings.py nella sezione DATABASES:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
```
È necessario che il database esista e che l’utente abbia i permessi adeguati per l’accesso e la modifica.

---

## Utilizzo
Dopo la configurazione, eseguire i seguenti comandi da terminale per applicare le migrazioni:
```bash
python manage.py makemigrations
python manage.py migrate
```
Una volta completato, si può avviare il server locale con:
```bash
manage.py runserver
```
L'applicazione sarà accessibile all'indirizzo: http://localhost:8000

## Web Application
L'applicativo apparirà ben o male così

<img width="1918" height="902" alt="image" src="https://github.com/user-attachments/assets/4be9f59a-3a54-4ccb-a5c6-5333eea3c4c8" />

<img width="667" height="839" alt="image" src="https://github.com/user-attachments/assets/8c31bff7-f985-4b03-a229-359e5eceb41a" />

---

## Licenza

Questo progetto è distribuito con licenza [MIT](LICENSE).  
Puoi usarlo, modificarlo e distribuirlo liberamente, a patto che venga mantenuta la nota di copyright.

---

## Utenti
vincydelucia04@gmail.com | Parthenope2025!
pierpaolo@pt.com | Parthenope2025!


