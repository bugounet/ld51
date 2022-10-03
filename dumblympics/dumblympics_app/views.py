from random import randint, random
from django.shortcuts import render, redirect
from django.forms import Form, CharField
from .models import Player, Race
from django.db import models
class NicknameForm(Form):
    nickname = CharField(max_length=50)
    
# Create your views here.
def index(request):
    form = NicknameForm(data=request.POST)
    if request.method == "POST" and form.is_valid():
        nickname= form.cleaned_data["nickname"]
        request.session["nickname"] = nickname
        request.session["uid"] = randint(0, 999999)
        race_id = Race.objects.get_or_create(open=True)[0].id
        Player.objects.update_or_create(race_id=race_id, nick=nickname, defaults={
            'uid': randint(0, 999999),
            'score': 0
        })
        return redirect("race", race_id)
    return render(request, 'dumblympics_app/index.html', {"nickname_form": form})

def race(request, race_id):
    return render(request, 'dumblympics_app/play.html', {
        'race_id': race_id,
        'nickname': request.session["nickname"],
        'uid': request.session["uid"]
    })
