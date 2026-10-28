from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from movies.models import Movie,Genre

def home(request):
    movies=Movie.objects.filter(is_upcoming=False).select_related('genre')[:12]
    upcoming=Movie.objects.filter(is_upcoming=True).select_related('genre')[:6]
    hero=movies.first()
    return render(request,'pages/home.html',{'movies':movies,'upcoming':upcoming,'hero':hero,'genres':Genre.objects.all()})
def about(request): return render(request,'pages/about.html')
@require_http_methods(['GET','POST'])
def contacts(request):
    if request.method=='POST':
        name=request.POST.get('name','').strip(); email=request.POST.get('email','').strip(); body=request.POST.get('message','').strip()
        if not name or '@' not in email or len(body)<10:
            return render(request,'pages/contacts.html',{'error':'Заполните имя, корректный email и сообщение от 10 символов.','values':request.POST})
        messages.success(request,'Спасибо за сообщение! (Демо-режим: отправка на email не подключена.)')
        return redirect('pages:thanks')
    return render(request,'pages/contacts.html')
def thanks(request): return render(request,'pages/thanks.html')
