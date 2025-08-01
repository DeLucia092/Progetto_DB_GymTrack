"""
URL configuration for GymTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FitStats.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #path('admin/', admin.site.urls)
   # path('',index, name='index'),
    path('', homepage, name='homepage'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('registration', scelta_registrazione, name='scelta_registrazione'),
    path('registration/cliente', registrazione_cliente, name='registrazione_cliente'),
    path('registration/trainer/', registrazione_trainer, name='registrazione_trainer'),
    path('creazione_schede/', creazione_schede, name='creazione_schede'),
    path('pagina_creazione_scheda/', pagina_creazione_scheda, name='pagina_creazione_scheda'),
    path('mie_schede/', mie_schede, name='mie_schede'),
    path('aggiungi_integratore/', aggiungi_integratore, name='aggiungi_integratore'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)