from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileImageForm, AboutForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .models import Recipe,UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse

# Create your views here.
@login_required
def dashboard_view(request):
    return render(request, 'recipeapp/dashboard.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'recipeapp/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')

    return render(request, 'recipeapp/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You’ve been logged out successfully.", extra_tags='logout')
    return redirect('login')

def search_view(request):
    return render(request, 'recipeapp/search.html')

def friends_view(request):
    return render(request, 'recipeapp/friends.html')

@login_required
def receipes_view(request):
    recipes = Recipe.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    favourite_recipes = profile.favourites.all()
    return render(request, 'recipeapp/receipes.html', {
        'recipes': recipes,
        'favourite_recipes': favourite_recipes
    })

@login_required
def account_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        about = request.POST.get('about')
        profile_pic = request.FILES.get('profile_pic')

        # Change Username
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, 'Username already exists.')
            else:
                user.username = new_username
                messages.success(request, 'Username changed successfully.')

        # Change Password
        if new_password:
            if user.check_password(new_password):
                messages.error(request, 'New password must be different from current password.')
            else:
                user.set_password(new_password)
                messages.success(request, 'Password changed successfully.')
                update_session_auth_hash(request, user)  # Stay logged in

        user.save()

        # Update About
        if about is not None:
            profile.about = about

        # Update Profile Picture
        if profile_pic:
            profile.profile_pic = profile_pic

        profile.save()
        return redirect('account')

    return render(request, 'recipeapp/account.html', {
        'user': user,
        'profile': profile
    })

def favourites_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    favourites = profile.favourites.all()
    return render(request, 'recipeapp/favourites.html', {'favourites': favourites})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    is_fav = False
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)

        is_fav = recipe in profile.favourites.all()

    ingredients_list = recipe.ingredients.strip().split('\n')
    return render(request, 'recipeapp/ingredients.html', {
        'recipe': recipe,
        'ingredients_list': ingredients_list,
        'is_fav': is_fav,
    })

@csrf_exempt
@login_required
def toggle_favourite(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(id=recipe_id)
        user_profile = request.user.userprofile

        if recipe in user_profile.favourites.all():
            user_profile.favourites.remove(recipe)
            return JsonResponse({'status': 'removed'})
        else:
            user_profile.favourites.add(recipe)
            return JsonResponse({'status': 'added'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def recipe_procedure(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    steps = recipe.procedure.strip().split('\n')
    return render(request, 'recipeapp/procedure.html', {
        'recipe': recipe,
        'steps': steps
    })


def search_recipes(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        recipes = Recipe.objects.filter(name__icontains=query)
        results = [{
            'id': r.id,
            'name': r.name,
            'url': reverse('recipe_detail', args=[r.id]),
        } for r in recipes]

    return JsonResponse({'recipes': results})
