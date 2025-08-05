from django.contrib import admin
from .models import Recipe,UserProfile

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'about']
    filter_horizontal = ['favourites']