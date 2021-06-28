from django.contrib import admin
from .models import Recipe, Track

admin.site.site_header = 'Recipe Tracker App'
admin.site.site_title = 'Recipe Tracks Admin Page'

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_name','user_name','created_date','visibility',)

# Register your models here.
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Track)

