from django.shortcuts import render


def conversion(request, origin_url, title):
    context = {"origin_url": origin_url, "title": title}
    return render(request, "theses/conversion.html", context)


def coaching_conversion(request):
    return render(request, "theses/coaching_conversion.html")
