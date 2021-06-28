from . import views
from django.urls import path

app_name = 'recipeViewer'
urlpatterns = [
    path('', views.home_view, name="home"),
    path('home', views.home_view, name="home_extended_url"),
    path('index',views.index, name = 'index'),
    path('search',views.searchView, name = 'search'),
    path('detail/<int:recipe_id>/', views.detailedRecipe, name='detailedViewer'),
    # add a view
    path('add/',views.create_recipe, name="create_recipe"),
    #edit the view
    path('update/<int:recipe_id>/', views.update_recipe, name="update_recipe"),
    #delete one item
    path('delete/<int:recipe_id>/', views.delete_recipe, name="delete_recipe"),
    #add one recipe track
    path('addTrack/',views.create_track, name="create_track"),
    #add a variation to a recipe
    path('addvariation/<int:recipe_id>/', views.add_recipe_variation, name="add_variation"),
    #remove the reference to a master recipe for the recipe given in parameter
    path('removevariation/<int:recipe_id>/', views.remove_recipe_variation, name="remove_variation"),

]
