from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django import forms
from django.shortcuts import redirect

from .models import *

def IndexView(request):
    ctx_lligues = Lliga.objects.all()

    return render(request,"lliga/index.html",
                {
                    "ctx_lligues":ctx_lligues,
                })    

def ClassificacioView(request,lliga_id):
    try:
        lliga = Lliga.objects.get(pk=lliga_id)
        equips = lliga.equips.all()
        ctx_classificacio = []
    
        # calculem punts en llista de tuples (equip,punts)
        for equip in equips:
            punts = 0
            for partit in lliga.partit_set.filter(local=equip):
                if partit.gols_local() > partit.gols_visitant():
                    punts += 3
                elif partit.gols_local() == partit.gols_visitant():
                    punts += 1
            for partit in lliga.partit_set.filter(visitant=equip):
                if partit.gols_local() < partit.gols_visitant():
                    punts += 3
                elif partit.gols_local() == partit.gols_visitant():
                    punts += 1
            ctx_classificacio.append( (punts,equip.nom) )
        # ordenem llista
        ctx_classificacio.sort(reverse=True)
    except LLiga.DoesNotExist:
        raise Http404("La lliga not existeix")

    return render(request,"lliga/classificacio.html",
                {
                    "ctx_classificacio":ctx_classificacio,
                })

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
 
def MenuView(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('lliga:classificacio', lliga.id)
    return render(request, "lliga/menu.html",{
                    "form": form,
            }) 
