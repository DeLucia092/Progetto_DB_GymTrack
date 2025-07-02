from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Utente(models.Model):
    class ruolo(models.TextChoices):
        Cliente = 'Cliente'
        PT = 'Personal Trainer'
    email=models.EmailField(max_length=200, primary_key=True, blank=False, null=False)
    password=models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=100, unique=True, blank=False, null=False)

    #PT
    stipendio = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    certificazione = models.ImageField(upload_to='certificazioni/', blank=True, null=True)

    #Cliente
    tipo_sport = models.CharField(max_length=100, blank=True, null=True)
    data_iscrizione = models.DateField(blank=True, null=True)
    scadenza_abbonamento = models.DateField(blank=True, null=True)
    stato_abbonamento = models.BooleanField(default=True)  # True se l'abbonamento è attivo, False se scaduto


class Esercizio(models.Model):
    nome= models.CharField(max_length=100, primary_key=True)
    gruppo_allenante = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=[
            ('petto', 'Petto'),
            ('spalle', 'Spalle'),
            ('bicipiti', 'Bicipiti'),
            ('tricipiti', 'Tricipiti'),
            ('quadricipiti', 'Quadricipiti'),
            ('femorali', 'Femorali'),
            ('addominali', 'Addominali'),
            ('schiena', 'Schiena'),
            ('polpacci', 'Polpacci'),
        ]
    )  # Gruppo muscolare allenato

class Preferenza(models.Model):
    nome_esercizio = models.ForeignKey(Esercizio, on_delete=models.CASCADE, related_name='preferenze')
    email_utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='preferenze')

    class Meta:
        unique_together = (('nome_esercizio', 'email_utente'),)

class Scheda(models.Model):
    id_scheda = models.IntegerField()
    nome_giornata = models.CharField(max_length=100)
    giorno_inizio = models.DateField(blank=False, null=False)
    giorno_fine = models.DateField(blank=False, null=False)
    email_utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='schede') #chiave esterna che collega la scheda all'utente
    creata_da = models.CharField(max_length=100)

    def clean(self):
        if not Utente.objects.filter(username=self.creata_da, ruolo='Personal Trainer').exists():
            raise ValidationError({'creata_da': 'Il nome inserito non corrisponde a un Personal Trainer registrato.'})

    class Meta:
        unique_together = (('id_scheda', 'nome_giornata'),)


class Composizione(models.Model):
    nome_esercizio = models.ForeignKey(Esercizio, on_delete=models.CASCADE, related_name='composizioni')
    scheda = models.ForeignKey(Scheda, on_delete=models.CASCADE, related_name='composizioni')
    #non metto anche nome_giornata perchè in django non è possibile avere una chiave esterna composta.
    #Scheda: collega la Composizione a una specifica riga di Scheda (che è identificata dalla coppia id_scheda e nome_giornata).
    serie_PT = models.IntegerField(default=0, blank=True, null=True)  # Numero di serie consigliate dal Personal Trainer
    tempo_recupero = models.IntegerField(default=60, blank=True, null=True)  # Tempo di recupero in secondi tra le serie
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True,null=True)  # Peso per l'esercizio
    ripetizioni = models.IntegerField(default=0, blank=True, null=True)  # Numero di ripetizioni
    class Meta:
        unique_together = (('scheda', 'nome_esercizio'),)

class Scheda_integratori(models.Model):
    id_scheda_integratori = models.AutoField(primary_key=True)
    email_utente = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='integratori')

class Integratore(models.Model):
    nome_integratore = models.CharField(max_length=100, primary_key=True)
    descrizione = models.TextField(blank=True, null=True)
    dosaggio = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Dosaggio giornaliero in grammi"
    )  # Dosaggio giornaliero in grammi

class Unione(models.Model):
    scheda_integratori = models.ForeignKey(Scheda_integratori, on_delete=models.CASCADE, related_name='unioni')
    nome_integratore = models.ForeignKey(Integratore, on_delete=models.CASCADE, related_name='unioni')

    class Meta:
        unique_together = (('scheda_integratori', 'nome_integratore'),)