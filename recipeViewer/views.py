from django.shortcuts import render,redirect, reverse
from django.db import models
from django.db.models import Q 
from .models import Recipe, Track
from .forms import RecipeForm, TrackForm, RecipeSearchForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.utils.translation import ugettext_lazy as _ 

import pdb

# Create your views here.
def index(request):
    #Recipe filter -> We will get all the PUBLIC recipes + all the recipes written by the current user
    if request.user.is_authenticated:
        recipe_list = Recipe.objects.filter(models.Q(visibility=Recipe.PUBLIC) | models.Q(user_name=request.user.id) ).order_by('-created_date')
    else:
        recipe_list = Recipe.objects.filter(visibility=Recipe.PUBLIC).order_by('-created_date')

    recipe_paginator = Paginator(recipe_list, Recipe.RECIPES_PER_PAGE)
    current_page = request.GET.get('page',1)
    try:
        recipe_list = recipe_paginator.page(current_page)
    except PageNotAnInteger:
        recipe_list = recipe_paginator.page(1)
    except EmptyPage:
        recipe_list = recipe_paginator.page(recipe_paginator.num_pages) 

    context = {
        'all_recipe_list' : recipe_list,
    }
    return render(request, 'recipeViewer/index.html', context)

def searchView(request):
    # Similar to the list view, except that we will display some form widgets
    
    if request.method == 'POST':
        # Looking at parameters, looking at a DB search, then filling the context with the return
        if request.user.is_authenticated:
            recipe_list = Recipe.objects.filter(models.Q(visibility=Recipe.PUBLIC) | models.Q(user_name=request.user.id) ).order_by('-created_date')
        else:
            recipe_list = Recipe.objects.filter(visibility=Recipe.PUBLIC).order_by('-created_date')
        
        search_parameters_form = RecipeSearchForm(request.POST)
        if search_parameters_form.is_valid():
            if not search_parameters_form.cleaned_data['include_variations_in_search']:
                recipe_list = recipe_list.filter(variation_of__isnull=True)
            if search_parameters_form.cleaned_data['name_filter'] != '':
                for parameter in search_parameters_form.cleaned_data['name_filter'].split(','):
                    recipe_list = recipe_list.filter(recipe_name__contains=parameter)
            if search_parameters_form.cleaned_data['tags_filter'] != '':
                for parameter in search_parameters_form.cleaned_data['tags_filter'].split(','):
                    recipe_list = recipe_list.filter(recipe_tags__contains=parameter)
            if search_parameters_form.cleaned_data['ingredients_filter'] != '':
                for parameter in search_parameters_form.cleaned_data['ingredients_filter'].split(','):
                    recipe_list = recipe_list.filter(ingredients__contains=parameter)

    else:
        # First display of the page, just need to create a blank context and display the files
        recipe_list = []
        search_parameters_form = RecipeSearchForm()
    
    context = { 'recipe_list' : recipe_list, 'form' : search_parameters_form, }

    return render(request, 'recipeViewer/recipe-search.html', context)

def detailedRecipe(request, recipe_id):
    #This view will show the details of a recipe
    recipe = Recipe.objects.get(pk = recipe_id)

    if recipe.user_name.id != request.user.id and recipe.visibility == Recipe.PRIVATE:
        messages.error( request, _("The recipe you are trying to access is private, you cannot access it!") )
        return redirect('recipeViewer:index')

    #Trying to be a bit clever -> parsing the tag list
    tag_list = recipe.recipe_tags.split(',')
    task_list = recipe.task_list.split(';')
    ingredients_list = recipe.ingredients.split('\n')

    track_list = recipe.tracks.filter(models.Q(visibility=Track.PUBLIC) | models.Q(user_id = request.user.id))
    track_form = TrackForm() 
    track_form.restrict_recipe(recipe_id)

    if len(recipe.variations.all()) != 0:
        variations_list = [r for r in recipe.variations.all() if (r.visibility == Recipe.PUBLIC) or (r.user_name == request.user )  ]
    elif recipe.variation_of is not None:
        # The list of variations in this case is the 'original' recipe + all the variations which are not the current one
        variations_list = [recipe.variation_of] + [r for r in recipe.variation_of.variations.all() if (r != recipe) and ((r.visibility == Recipe.PUBLIC) or (r.user_name == request.user ))  ]
    else:
        variations_list = []

    context = {
        'recipe':recipe,
        'tag_list': tag_list,
        'task_list' : task_list,
        'ingredients_list' : ingredients_list,
        'track_list' : track_list,
        'track_form' : track_form,
        'variations_list' : variations_list,
    }
    return render(request, 'recipeViewer/recipeDetail.html', context)

@login_required
def create_recipe(request):
    #This view will help create a form with a new recipe
    if request.method == 'POST':
        current_form = RecipeForm(request.POST, request.FILES)
        #Validity check of the form
        if current_form.is_valid():
            newRecipe = current_form.save()
            newRecipe.user_name = request.user
            newRecipe.save()
            return redirect(newRecipe)
    else:
        current_form = RecipeForm()

    return render(request, 'recipeViewer/recipe-form.html', { 'form' : current_form })

@login_required
def update_recipe(request, recipe_id):
    #This view will help edit an object
    
    recipe = Recipe.objects.get(pk=recipe_id)
    # Safety to prevent users from editing recipes they don't own
    if recipe.user_name.id != request.user.id:
        messages.error( request, _("You are not autorized to update a recipe you don't own") )
        return redirect('recipeViewer:index')

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipeViewer:index')
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipeViewer/recipe-form.html', { 'form':form, 'recipe':recipe })

@login_required
def delete_recipe(request, recipe_id):
    #Delete the id
    recipe = Recipe.objects.get(pk = recipe_id)

    # Safety to prevent users from editing recipes they don't own
    if recipe.user_name.id != request.user.id:
        messages.error( request, _("You are not autorized to delete a recipe you don't own") )
        return redirect('recipeViewer:index')

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipeViewer:index')

    return render(request, 'recipeViewer/recipe-delete.html', {'recipe' : recipe})   

@login_required
def add_recipe_variation(request, recipe_id):
    #This view will help create a form with a new recipe
    if request.method == 'POST':
        current_form = RecipeForm(request.POST, request.FILES)
        #Validity check of the form
        if current_form.is_valid():
            # TO DO -> A lot of exception handling for unexcepted cases below
            newRecipe = current_form.save()
            newRecipe.user_name = request.user
            masterRecipe = Recipe.objects.get(pk=recipe_id)
            if masterRecipe.variation_of is None:
                newRecipe.variation_of = masterRecipe
            else:
                newRecipe.variation_of = masterRecipe.variation_of # Flattening the tree: a variation of a variation is a variation of the original recipe
            newRecipe.save()
            return redirect(newRecipe)
    else:
        master_recipe = Recipe.objects.get(pk=recipe_id) 
        current_form = RecipeForm(initial={'recipe_name': master_recipe.recipe_name , 'recipe_tags' : master_recipe.recipe_tags, \
            'ingredients' : master_recipe.ingredients, 'task_list' : master_recipe.task_list})

    return render(request, 'recipeViewer/recipe-form.html', { 'form' : current_form })

@login_required
def remove_recipe_variation(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    if recipe.user_name == request.user:
        if not recipe.variation_of is None:
            recipe.variation_of = None
            recipe.save()
    else:
        # User not allowed to edit the recipe
        messages.error( request, _("You are not autorized to delete a recipe you don't own") )
    return redirect(recipe)

def home_view(request):
    # This is the view which will correspond to the welcome page, with some static content and some edited stuff
    top_three_recipes = Recipe.objects.filter(visibility=Recipe.PUBLIC).order_by('-created_date')[:3]
    context = { 'top_recipe_list' : top_three_recipes, }

    return render(request, 'recipeViewer/home.html', context)

@login_required
def create_track(request):
    
    if request.method == 'POST':
        new_track_form = TrackForm(request.POST)

        if new_track_form.is_valid():
            newTrack = new_track_form.save(commit=False)
            newTrack.user_id = User.objects.get(pk=request.user.id)
            # Validation check -> We need to check if the corresponding recipe exists, if it is public or owned by the corresponding user
            try:
                newTrack.recipe_id = new_track_form.cleaned_data['recipe_id'] # The cleaned data contains the actual object
                if newTrack.recipe_id.visibility == Recipe.PUBLIC or newTrack.recipe_id.user_name.id == request.user.id:
                    # Then we can create the track
                    newTrack.save()
                    return redirect('recipeViewer:detailedViewer', recipe_id=newTrack.recipe_id.id)
                else:
                    messages.warning(request, _('Cannot create the Recipe Track - Not authorized') )
                    return redirect('recipeViewer:detailedViewer', recipe_id=newTrack.recipe_id.id)
            except ObjectDoesNotExist:
                messages.error(request,_('Cannot find the corresponding recipe'))
                return redirect('home')
        else:
            messages.info(request,_('Invalid form'))
    else:
        new_track_form = TrackForm()
    
    return render(request, 'recipeViewer/track-form.html', { 'form' : new_track_form,  })
