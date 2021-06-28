from django.test import TestCase
from datetime import datetime

from recipeViewer.models import Recipe

# Create your tests here.

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Recipe.objects.create(recipe_name='Bechamel',ingredients='Farine(50g), Butter(50g), Milk (500 ml)', recipe_tags='french,basic,technique', task_list='Melt butter in a pan.;Switch off heat and mix flour;Pour milk little by little and bring to a boil')

    def test_recipe_name_label(self):
        first_recipe = Recipe.objects.get(pk=1)
        field_label = first_recipe._meta.get_field('recipe_name').verbose_name
        self.assertEquals(field_label, 'recipe name')

    def test_recipe_string_is_recipe_name(self):
        first_recipe = Recipe.objects.get(pk=1)
        expected_label = '%s' % first_recipe.recipe_name
        self.assertEquals(expected_label, str(first_recipe))
    
    def test_get_absolute_url(self):
        first_recipe = Recipe.objects.get(pk=1)
        self.assertEquals(first_recipe.get_absolute_url(),'/recipeviewer/detail/1/')
    
    def test_default_visibility_private(self):
        first_recipe = Recipe.objects.get(pk=1)
        self.assertEquals(first_recipe.visibility, Recipe.PRIVATE)
    
    def test_default_created_date_is_same_than_today(self):
        first_recipe = Recipe.objects.get(pk=1)
        self.assertEquals(first_recipe.created_date.day,datetime.today().day)
        self.assertEquals(first_recipe.created_date.month,datetime.today().month)
        self.assertEquals(first_recipe.created_date.year,datetime.today().year)
        self.assertEquals(first_recipe.created_date.hour,datetime.now().hour)
        self.assertEquals(first_recipe.created_date.minute,datetime.now().minute)
    
    
        