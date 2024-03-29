from django.shortcuts import render, HttpResponseRedirect
from . import models
from django.http import HttpResponse, FileResponse
from .forms import capteurForm
from .models import data
import csv
from fpdf import FPDF

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    data = list(models.data.objects.all())
    count = len(data)
    for i in data:
        capteur = models.capteur.objects.get(id=i.capteur)
        i.piece = capteur.piece
        i.emplacement = capteur.emplacement
        i.capteur_nom = capteur.nom
    data.reverse()
    return render(request, 'index.html',{'data':data,'count':count})

def update(request,id):
    if request.method == "POST":
        form = capteurForm(request.POST)
        if form.is_valid():
            capteur = form.save(commit=False)
            capteur.id = id
            capteur.piece = models.capteur.objects.get(pk=id).piece
            capteur.save()
            return HttpResponseRedirect("/capteurs")
    else:
        capteur = models.capteur.objects.get(pk=id)
        form = capteurForm(capteur.dico())
        return render(request,"update.html",{"form":form, "id":id, "capteur": capteur})


def index_capteurs(request):
    data = list(models.capteur.objects.all())
    count = len(data)
    return render(request, 'index_capteurs.html', {'liste': data, 'count': count})

def mesures_capteurs(request,id):
    data = list(models.data.objects.filter(capteur=id))
    count = len(data)
    for i in data:
        capteur = models.capteur.objects.get(id=i.capteur)
        i.piece = capteur.piece
        i.emplacement = capteur.emplacement
        i.capteur_nom = capteur.nom
    data.reverse()
    return render(request, 'index.html', {'data': data, 'count': count,'id':id})

def delete_capteur(request,id):
    capteur = models.capteur.objects.get(pk=id)
    data = list(models.data.objects.filter(capteur=id))
    for i in data:
        i.delete()
    capteur.delete()
    return HttpResponseRedirect('/capteurs')

def charts(request):
    liste = list(models.capteur.objects.all())
    c1 = []
    c2 = []
    data = list(models.data.objects.all())
    for i in data:
        capteur = models.capteur.objects.get(id=i.capteur)
        if int(i.capteur) == 1:
            c1.append(i)
        elif int(i.capteur) == 2:
            c2.append(i)
    return render(request, 'charts.html',{'liste1':c1,'liste2':c2})

def export(request,id):
    capteur = models.capteur.objects.get(pk=id)
    data = models.data.objects.filter(capteur=id)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=16)
    pdf.cell(200, 10, txt="Voici les éléments de notre capteur :", ln=2, align='C')
    for i in range(0,len(data)):
        pdf.cell(200,10,txt="Mesure " + str(i+1) + ": " + " TEMPERATURE" + str(data[i].data) + ", TIMESTAMP" + str(data[i].timestamp) , ln = 2+i, align='C')
    pdf.output('SAE24.pdf')
    response = FileResponse(open("SAE24.pdf"))
    return response