import euterpe_django.settings as settings
from django.http import HttpResponse
from django.shortcuts import render
import datetime
import json
import os


def home(request):
    return render(request, 'platforma/index.html')


def generate_music(genre):
    os.chdir('../')
    os.system('./skrypt.sh {}'.format(genre))
    polecenie = 'mv piece.wav {}/{}.wav'.format(settings.MEDIA_ROOT,
                                                '{0}-{1}'.format(genre, str(
                                                    datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")))
                                                )
    os.system(polecenie)
    os.chdir('euterpe_django')
    return


def lista(request):
    os.chdir(settings.MEDIA_ROOT)
    lista_utworow = list(os.listdir('.'))
    print(lista_utworow)
    os.chdir('../')
    return render(request, 'platforma/list.html', {'lista': lista_utworow})


def endpoint(request):
    genre = request.POST.get('genre', 'null')
    if genre != 'null':
        generate_music(genre)
    return HttpResponse(json.dumps({
        'status': 'success'
    }), content_type='application/json')
