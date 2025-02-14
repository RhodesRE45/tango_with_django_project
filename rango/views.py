from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed_pages = Page.objects.order_by('-views')[:5]

    if 'visits' not in request.session:
        request.session['visits'] = 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = request.session['visits']
        last_visit_str = request.session.get('last_visit', str(datetime.now()))
        last_visit_time = datetime.strptime(last_visit_str, "%Y-%m-%d %H:%M:%S.%f")

        if (datetime.now() - last_visit_time).days > 0:
            visits += 1
            request.session['visits'] = visits
            request.session['last_visit'] = str(datetime.now())

    request.session.modified = True

    context_dict = {
        'categories': category_list,
        'most_viewed_pages': most_viewed_pages,
        'user': request.user,
    }

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    if 'visits' not in request.session:
        request.session['visits'] = 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = request.session['visits']
        last_visit_str = request.session.get('last_visit', str(datetime.now()))
        last_visit_time = datetime.strptime(last_visit_str, "%Y-%m-%d %H:%M:%S.%f")

        if (datetime.now() - last_visit_time).days > 0:
            visits += 1
            request.session['visits'] = visits
            request.session['last_visit'] = str(datetime.now())

    request.session.modified = True

    return render(request, 'rango/about.html', {'visits': request.session['visits']})


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/show_category.html', context=context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.name)
            category.save()
            return redirect('rango:index')
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.slug = slugify(page.title)
            page.save()
            return redirect('rango:show_category', category_name_slug=category.slug)
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('rango:index')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('rango:index')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

