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
    batch_detection
)
from django.http import JsonResponse


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
        "requiredAttr": ["target"]
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
        translator = request.POST.get('translator')
        source_language = request.POST.get('source')

        # Default translator is google
        if not translator:
            translator = 'google'

        if not translators[translator]:
            return JsonResponse({'error': 'incorrect translator'})

        if not source_language:
            return JsonResponse({'error': 'Source language required : fill with "auto" if you don\'t know...'})

        text = request.POST.get('text')
        if text:
            # Check if all params are present (depends on current translator)
            missing_params = []
            for attr in translators[translator]["requiredAttr"] or []:
                if not request.POST.get(attr):
                    missing_params.append(attr)

            if len(missing_params) > 0:
                return JsonResponse({'error': 'missing attribute: ' + ", ".join(missing_params)})

            target_translator = translators[translator]["translator"](source=source_language, target=target_language)
            translation = target_translator.translate(text)
        else:
            translation = ""
        payload = {'result': translation}
        return JsonResponse(payload)
