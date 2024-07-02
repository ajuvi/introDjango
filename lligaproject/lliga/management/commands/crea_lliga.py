from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import timedelta, datetime
from random import randint
import random

from lliga.models import *

faker = Faker(["es_CA", "es_ES"])
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

    def random_datetime(self, start, end):
        delta = end - start
        int_delta = int(delta.total_seconds())
        random_second = random.randrange(int_delta)
        naive_datetime = start + timedelta(seconds=random_second)
        return timezone.make_aware(naive_datetime, timezone.get_current_timezone())

    def create_lliga(self, nom_lliga):
        current_year = timezone.now().year
        temporada = f"{current_year}/{current_year + 1}"

        lliga = Lliga(
            nom=nom_lliga,
            data_inici=timezone.now(),
            data_final=timezone.now() + timedelta(days=11 * 30),
            temporada=temporada,
            pais=faker.country()
        )
        lliga.save()
        return lliga

    def create_equip(self, lliga):
        ciutat = faker.city()
        prefix = random.choice(data_prefixos)
        if prefix:
            prefix += " "
        nom = prefix + ciutat
        equip = Equip(
            ciutat=ciutat,
            nom=nom,
            entrenador=faker.name(),
            estadi=faker.company(),
            any_fundacio=randint(1900, timezone.now().year),
            lliga=lliga
        )
        equip.save()
        lliga.equips.add(equip)
        return equip

    def create_jugadors(self, equip):
        for _ in range(25):
            jugador = Jugador(
                nom=faker.name(),
                posicio=random.choice(data_posicions),
                edat=faker.random_int(min=16, max=40),
                nacionalitat=faker.country(),
                equip=equip
            )
            jugador.save()

    def create_partits(self, lliga):
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local != visitant:
                    partit_inici = self.random_datetime(
                        datetime.combine(lliga.data_inici, datetime.min.time()),
                        datetime.combine(lliga.data_final, datetime.max.time())
                    )
                    partit = Partit(local=local, visitant=visitant, lliga=lliga, inici=partit_inici)
                    partit.save()
                    self.create_events(partit, local, visitant)

    def create_events(self, partit, local, visitant):
        num_events = randint(5, 20)
        for _ in range(num_events):
            minutes_event = randint(0, 180)
            temps_event = partit.inici + timedelta(minutes=minutes_event)
            tipus_event = random.choice(data_events)
            jugador_local = faker.random_element(elements=local.jugadors.all())
            jugador_visitant = faker.random_element(elements=visitant.jugadors.all())

            jugador1 = jugador_local
            jugador2 = jugador_visitant

            if random.random() < 0.5:
                jugador1 = jugador_visitant
                jugador2 = jugador_local

            if random.random() < 0.5:
                tipus_event = Event.EventType.GOL

            event = Event(
                partit=partit,
                temps=temps_event,
                tipus=tipus_event,
                jugador=jugador1,
                equip=jugador1.equip,
                jugador2=jugador2,
            )
            event.save()
            print(f'Creat event {event}')

    def handle(self, *args, **options):
        nom_lliga = options['nom_lliga'][0]
        lliga = Lliga.objects.filter(nom=nom_lliga)
        if lliga.count() > 0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return

        print(f"Creem la nova lliga: {nom_lliga}")
        lliga = self.create_lliga(nom_lliga)

        print("Creem equips")
        for _ in range(20):
            equip = self.create_equip(lliga)
            print(f"Creem jugadors de l'equip {equip.nom}")
            self.create_jugadors(equip)

        print("Creem partits de la lliga")
        self.create_partits(lliga)
