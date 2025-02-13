from django.shortcuts import render, get_object_or_404
from rango.models import Category, Page

def index(request):
    context_dict = {'message': "Rango says hello world!"}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]  # Get the top 5 most popular categories
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context=context_dict)


def show_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)  # Acquisition sort
    pages = Page.objects.filter(category=category)  # Gets all pages in this category

    context_dict = {
        'category': category,
        'pages': pages
    }

    return render(request, 'rango/category.html', context=context_dict)