import imp
from django.shortcuts import render
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)
from django.http import JsonResponse
import json
import iso639

# Create your views here.
def home(request):
    return render(request, 'home.html')


def translate(request):
    if request.method == "POST":
        target_language = request.POST.get('tar-lang');
        if request.POST.get('text'):
            translation = GoogleTranslator(target=target_language).translate(request.POST.get('text', ''))
        else:
            translation = ""
        payload = {'result': translation}
        return JsonResponse(payload)
