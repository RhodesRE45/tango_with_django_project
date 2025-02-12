from django.shortcuts import render

def index(request):
    context_dict = {'message': "Rango says hello world!"}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')