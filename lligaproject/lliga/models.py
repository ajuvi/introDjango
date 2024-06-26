from django.db import models

class Lliga(models.Model):
    nom = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    temporada = models.CharField(max_length=255)
    numero_d_equips = models.IntegerField()

    def __str__(self):
        return self.nom

class Equip(models.Model):
    nom = models.CharField(max_length=255)
    estadi = models.CharField(max_length=255)
    entrenador = models.CharField(max_length=255)
    any_fundacio = models.IntegerField()
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name='equips')

    def __str__(self):
        return self.nom

class Jugador(models.Model):
    nom = models.CharField(max_length=255)
    posicio = models.CharField(max_length=255)
    edat = models.IntegerField()
    nacionalitat = models.CharField(max_length=255)
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='jugadors')
    estadistiques = models.JSONField()

    def __str__(self):
        return self.nom

class Partit(models.Model):
    data = models.DateField()
    equip_local = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='partits_locals')
    equip_visitant = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='partits_visitants')
    marcador = models.CharField(max_length=10)
    estadi = models.CharField(max_length=255)
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name='partits')

    def __str__(self):
        return f'{self.equip_local} vs {self.equip_visitant} - {self.data}'
    
    def gols_local(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equip=self.equip_local).count() 

    def gols_visitant(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equip=self.equip_visitant).count()  

class Event(models.Model):
    # el tipus d'event l'implementem amb algo tipus "enum"
    class EventType(models.TextChoices):
        GOL = "GOL"
        AUTOGOL = "AUTOGOL"
        FALTA = "FALTA"
        PENALTY = "PENALTY"
        MANS = "MANS"
        CESSIO = "CESSIO"
        FORA_DE_JOC = "FORA_DE_JOC"
        ASSISTENCIA = "ASSISTENCIA"
        TARGETA_GROGA = "TARGETA_GROGA"
        TARGETA_VERMELLA = "TARGETA_VERMELLA"
    partit = models.ForeignKey(Partit,on_delete=models.CASCADE)
    temps = models.TimeField()
    tipus = models.CharField(max_length=30,choices=EventType.choices)
    jugador = models.ForeignKey(Jugador,null=True,
                    on_delete=models.SET_NULL,
                    related_name="events_fets")
    equip = models.ForeignKey(Equip,null=True,
                    on_delete=models.SET_NULL)
    # per les faltes
    jugador2 = models.ForeignKey(Jugador,null=True,blank=True,
                    on_delete=models.SET_NULL,
                    related_name="events_rebuts")
    detalls = models.TextField(null=True,blank=True)