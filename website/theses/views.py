from django.shortcuts import render


def conversion(request, origin_url, title):
    context = {
        'origin_url': origin_url,
        'title': title,
    }
    return render(request, 'theses/conversion.html', context)
