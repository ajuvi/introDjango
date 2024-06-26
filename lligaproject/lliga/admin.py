from django.contrib import admin

# Register your models here.

from .models import *


class EventInline(admin.TabularInline):
	model = Event
	fields = ["temps","tipus","jugador","equip"]
	ordering = ("temps",)
class PartitAdmin(admin.ModelAdmin):
        # podem fer cerques en els models relacionats
        # (noms dels equips o títol de la lliga)
	search_fields = ["local__nom","visitant__nom","lliga__titol"]
        # el camp personalitzat ("resultats" o recompte de gols)
        # el mostrem com a "readonly_field"
	readonly_fields = ["resultat",]
	list_display = ["local","visitant","resultat","lliga","inici"]
	ordering = ("-inici",)
	inlines = [EventInline,]
	def resultat(self,obj):
		gols_local = obj.gols_local()
		gols_visit = obj.gols_visitant()
		return "{} - {}".format(gols_local,gols_visit)
 
admin.site.register(Partit,PartitAdmin)
#admin.site.register(Partit)

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)
admin.site.register(Event)