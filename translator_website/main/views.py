import imp
from django.shortcuts import render
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             QCRI,
                             single_detection,
                             batch_detection)
from django.http import JsonResponse
import json
import iso639

EngineSelector = {
    '': GoogleTranslator,
    'Google Translate': GoogleTranslator,
    'Microsoft Translate': MicrosoftTranslator,
    'MyMemory Translate': MyMemoryTranslator,
    'PONS Translate': PonsTranslator,
    'Linguee Translate': LingueeTranslator,
    'Yandex Translate': YandexTranslator,
    'Papago Translate': PapagoTranslator
    # 'Deepl Translate': DeeplTranslator
}

# Create your views here.
def home(request):
    return render(request, 'home.html')

def app(request):
    return render(request, 'app.html')


def getLanguages(request):
    if request.method == "POST":
        Engine = EngineSelector[request.POST.get('engine')]
        languages = Engine.get_supported_languages(as_dict=True)
        return JsonResponse(data=languages)

def translate(request):
    if request.method == "POST":
        target_language = request.POST.get('tar-lang')
        if request.POST.get('text'):
            print(EngineSelector[request.POST.get('engine', '')])
            translation = EngineSelector[request.POST.get('t-engine', '')](target=target_language).translate(request.POST.get('text', ''))
        else:
            translation = ""
        payload = {'result': translation}
        return JsonResponse(payload)
