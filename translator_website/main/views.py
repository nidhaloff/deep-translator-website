from deep_translator.exceptions import ElementNotFoundInGetRequest, RequestError
from dotenv import dotenv_values
from django.shortcuts import render
from deep_translator import (
    GoogleTranslator,
    MicrosoftTranslator,
    PonsTranslator,
    LingueeTranslator,
    MyMemoryTranslator,
    YandexTranslator,
    PapagoTranslator,
    DeeplTranslator,
    QcriTranslator,
    single_detection,
    batch_detection,
)
from django.http import JsonResponse

config = dotenv_values(".env")


# Create your views here.
def home(request):
    return render(request, 'home.html')


translators = {
    'google': {
        "translator": GoogleTranslator,
        "requiredAttr": ["target"]
    },
    'microsoft': {
        "translator": MicrosoftTranslator,
        "requiredAttr": ["target", "api_key"]
    },
    'pons': {
        "translator": PonsTranslator,
        "requiredAttr": ["target"],
    },
    'linguee': {
        "translator": LingueeTranslator,
        "requiredAttr": ["target"]
    },
    'mymemory': {
        "translator": MyMemoryTranslator,
        "requiredAttr": ["target"]
    },
    'yandex': {
        "translator": YandexTranslator,
        "requiredAttr": ["api_key"]
    },
    'papago': {
        "translator": PapagoTranslator,
        "requiredAttr": ["target", "secret_key", "client_id"]
    },
    'deepl': {
        "translator": DeeplTranslator,
        "requiredAttr": ["api_key"]
    },
    'qcri': {
        "translator": QcriTranslator,
        "requiredAttr": ["target", "api_key"]
    }
}


def translate(request):
    if request.method == "POST":
        # Get POST params
        target_language = request.POST.get('target')
        passed_translators = request.POST.getlist('translators[]')
        source_language = request.POST.get('source')
        text = request.POST.get('text')
        if not text or text == "":
            return JsonResponse({})
        if not source_language:
            return JsonResponse({'error': 'Source language required : fill with "auto" if you don\'t know...'})

        result = {}
        for translator in passed_translators:
            translation = translate_by_translator(request, translator, source_language, target_language, text)
            if translation is not None:
                result[translator] = translation
        return JsonResponse(result)


def translate_by_translator(request, translator, source_language, target_language, text):
    try:
        # Default translator is google
        if not translator:
            translator = 'google'

        if not translators[translator]:
            return JsonResponse({'error': 'incorrect translator'})

        params_to_give = [source_language]
        if target_language is not None:
            params_to_give.append(target_language)
        for attr in translators[translator]["requiredAttr"] or []:
            cur_atr = request.POST.get(attr)
            if not cur_atr:
                env_param = config.get(translator.upper() + "_" + attr.upper())
                if env_param is None or env_param == "":
                    return
                else:
                    if env_param not in params_to_give:
                        params_to_give.append(env_param)
            else:
                if cur_atr not in params_to_give:
                    params_to_give.append(cur_atr)

        target_translator = translators[translator]["translator"](*params_to_give)
        translation = target_translator.translate(text)

        return translation
    except ElementNotFoundInGetRequest or RequestError or Exception:
        return
