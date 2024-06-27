from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint
import random
 
from lliga.models import *
 
faker = Faker(["es_CA","es_ES"])
data_posicions = ["Porter", "Defensa", "Migcampista", "Davanter"]
data_prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
data_events = [
            Event.EventType.GOL,
            Event.EventType.AUTOGOL,
            Event.EventType.FALTA,
            Event.EventType.PENALTY,
            Event.EventType.MANS,
            Event.EventType.CESSIO,
            Event.EventType.FORA_DE_JOC,
            Event.EventType.ASSISTENCIA,
            Event.EventType.TARGETA_GROGA,
            Event.EventType.TARGETA_VERMELLA
        ]

class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'

    def add_arguments(self, parser):
        parser.add_argument('nom_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        nom_lliga = options['nom_lliga'][0]
        lliga = Lliga.objects.filter(nom=nom_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return

        print(f"Creem la nova lliga: {nom_lliga}")
        print("----------")            
        
        current_year = timezone.now().year
        temporada = f"{current_year}/{current_year + 1}"

        lliga = Lliga(  nom=nom_lliga,
                        data_inici=timezone.now(),
                        data_final=timezone.now()+timedelta(days=11*30),
                        temporada=temporada,
                        pais=faker.country())
        lliga.save()

        print("Creem equips")
        print("----------")                    
        for i in range(20):
            ciutat = faker.city()
            prefix =  random.choice(data_prefixos)
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            equip = Equip(
                ciutat=ciutat,
                nom=nom, 
                entrenador=faker.name(),
                estadi=faker.company(),
                any_fundacio=randint(1900, current_year),
                lliga=lliga
            )
            print(equip)
            equip.save()
            lliga.equips.add(equip)

            print("Creem jugadors de l'equip "+nom)
            print("----------")            
            for j in range(25):
                jugador = Jugador(
                    nom=faker.name(),
                    posicio=random.choice(data_posicions),  
                    edat=faker.random_int(min=16, max=40), 
                    nacionalitat=faker.country(), 
                    equip=equip
                )
                print(jugador)
                jugador.save()

        print("Creem partits de la lliga")
        print("----------") 
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local!=visitant:
                    partit = Partit(local=local,visitant=visitant)
                    partit.local = local
                    partit.visitant = visitant
                    partit.lliga = lliga
                    partit.save()

                    # Crear events
                    print("Creem els events del partit")                    
                    print("----------")
                    num_events=randint(5, 200)
                    for _ in range(num_events):
                        temps_event = faker.date_time_between_dates(datetime_start=partit.inici, datetime_end=partit.inici + timedelta(minutes=180))
                        tipus_event = random.choice(data_events)
                        jugador_local = faker.random_element(elements=local.jugadors.all())
                        jugador_visitant = faker.random_element(elements=visitant.jugadors.all())

                        jugador1=jugador_local
                        jugador2=jugador_visitant                            

                        if random.random() < 0.5:
                            jugador1=jugador_visitant
                            jugador2=jugador_local                            

                        event = Event(
                            partit=partit,
                            temps=temps_event,
                            tipus=tipus_event,
                            jugador=jugador_local if faker.boolean(chance_of_getting_true=50) else jugador_visitant,
                            equip=local if faker.boolean(chance_of_getting_true=50) else visitant,
                            jugador2=jugador_visitant if tipus_event == Event.EventType.FALTA else None,
                        )