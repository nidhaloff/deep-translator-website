from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from deep_translator import GoogleTranslator


def home(request):
    return render(request, 'website/home.html')


def translate(request):
    if request.method == "POST":
        text = request.POST.get("text")
        source = request.POST.get("source")
        target = request.POST.get("target")
        translator = request.POST.get("translator")

        print(text, source, target, translator)

        # Check if a parameter is missing
        if not text or not source or not target or not translator:
            return JsonResponse({"text": ""})

        try:
            # Translate the text. TODO : Add code from the previous version, to this file :) (without removing the
            #  existing one !!!)
            translated = GoogleTranslator(source=source, target=target).translate(text)
            return JsonResponse({"text": translated})
        except Exception as e:
            print(e)
            return JsonResponse({"text": ""})
