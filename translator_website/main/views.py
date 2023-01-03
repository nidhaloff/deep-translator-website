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
    batch_detection
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
        print("target : " + target_language + " source : " + source_language + " translator : " + translator)

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
            params_to_give = [source_language]
            if target_language is not None:
                params_to_give.append(target_language)
            for attr in translators[translator]["requiredAttr"] or []:
                cur_atr = request.POST.get(attr)
                if not cur_atr:
                    # Check if current param is in .env
                    print("PARAM IN ENV ? : " + config.get("DEEPL_API_KEY"))
                    env_param = config.get("DEEPL_API_KEY")
                    if env_param is None:
                        missing_params.append(attr)
                    else:
                        if env_param not in params_to_give:
                            params_to_give.append(env_param)
                else:
                    if cur_atr not in params_to_give:
                        params_to_give.append(cur_atr)

            if len(missing_params) > 0:
                return JsonResponse({'error': 'missing attribute: ' + ", ".join(missing_params)})
            print(params_to_give)

            target_translator = translators[translator]["translator"](*params_to_give)
            translation = target_translator.translate(text)
        else:
            translation = ""
        payload = {'result': translation}
        return JsonResponse(payload)
