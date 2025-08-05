from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('account/', views.account_view, name='account'),
    path('search/',views.search_view, name='search'),
    path('friends/', views.friends_view, name='friends'),
    path('receipes/', views.receipes_view, name='receipes'),
    path('toggle-favourite/<int:recipe_id>/', views.toggle_favourite, name='toggle_favourite'),
    path('favourites/', views.favourites_view, name='favourites'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('search-recipes/', views.search_recipes, name='search_recipes'),
    path('toggle-favourite/<int:recipe_id>/', views.toggle_favourite, name='toggle_favourite'),
    path('recipe/<int:pk>/procedure/', views.recipe_procedure, name='recipe_procedure'),
]
