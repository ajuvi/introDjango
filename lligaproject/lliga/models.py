from django.db import models

class Lliga(models.Model):
    nom = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    temporada = models.CharField(max_length=255)
    data_inici = models.DateField()
    data_final = models.DateField()    

    def __str__(self):
        return f"{self.nom} {self.temporada}" 

    def numero_equips(self):
        return self.equips.count()

class Equip(models.Model):
    nom = models.CharField(max_length=255)
    ciutat = models.CharField(max_length=255)
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

    def __str__(self):
        return self.nom

class Partit(models.Model):
    class Meta:
        unique_together = ["local","visitant","lliga"]
    local = models.ForeignKey(Equip,on_delete=models.CASCADE,
                    related_name="partits_local")
    visitant = models.ForeignKey(Equip,on_delete=models.CASCADE,
                    related_name="partits_visitant")
    lliga = models.ForeignKey(Lliga,on_delete=models.CASCADE)
    detalls = models.TextField(null=True,blank=True)
    inici = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return "{} - {}".format(self.local,self.visitant)

    def gols_local(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equip=self.local).count()

    def gols_visitant(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equip=self.visitant).count()

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


    def __str__(self):
        return f"{self.tipus} - {self.partit} - {self.jugador}"
