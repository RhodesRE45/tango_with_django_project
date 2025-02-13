import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page

def populate():
    python_cat = add_cat("Python", views=128, likes=64)

    add_page(cat=python_cat, title="Official Python Docs",
             url="https://docs.python.org/3/")

    django_cat = add_cat("Django", views=64, likes=32)

    add_page(cat=django_cat, title="Django Documentation",
             url="https://docs.djangoproject.com/en/2.2/")

    print("Database populated!")

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
