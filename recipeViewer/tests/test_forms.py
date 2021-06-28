from django.test import TestCase
from django.urls import reverse

from recipeViewer.models import Recipe, Track
from recipeViewer.forms import RecipeForm

from django.contrib.auth.models import User

# Create your tests here.

class test_create_view_and_form(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='gluglu1')
        test_user2 = User.objects.create_user(username='testuser2', password='gluglu2')
       
        first_recipe = Recipe.objects.create(recipe_name='Test Public Recipe 1',ingredients='butter,flour,cherries', recipe_tags='french,japanese', task_list='Task1;Task2;Task3', \
                visibility=Recipe.PUBLIC, user_name=test_user1)
        second_recipe = Recipe.objects.create(recipe_name='Test Public Recipe 2',ingredients='raisins,walnuts,peanuts', recipe_tags='mexican,vegan', task_list='Task1;Task2;Task3', \
                visibility=Recipe.PRIVATE, user_name=test_user2)

    # def test_create_at_desired_location(self):
    #     login1 = self.client.login(username='testuser1', password='gluglu1')
    #     response = self.client.get('/recipeviewer/add/')
    #     self.assertEquals(response.status_code,200)
    #     self.client.logout
    #     response = self.client.get('/recipeviewer/add/', follow=True)
    #     self.assertRedirects(response, '/login?',status_code=200, target_status_code=200)
    
    def test_create_recipe_post_request(self):
        login1 = self.client.login(username='testuser1', password='gluglu1')
        user1 = User.objects.get(username='testuser1')
        # Test of proper input and satisfactory result (we look into the DB to see if the result is there)
        response = self.client.post('/recipeviewer/add/',{ 'recipe_name' : 'choux', 'ingredients' : '50g flour, 3 eggs, 100g butter', 'recipe_tags' : 'french, pastry', \
            'task_list' : '1. look at the stuff; 2. get the things done', 'user_name' : user1, 'visibility' : Recipe.PUBLIC  })
        
        recipe_choux = Recipe.objects.get(recipe_name__contains='choux')
        self.assertEquals(recipe_choux.ingredients,'50g flour, 3 eggs, 100g butter')
        self.assertEquals(recipe_choux.recipe_tags,'french, pastry')
        self.assertEquals(recipe_choux.task_list,'1. look at the stuff; 2. get the things done')

        # Test of wrong input -> we forget the 
        response = self.client.post('/recipeviewer/add/',{ 'recipe_name' : 'choux',  'user_name' : user1, 'visibility' : Recipe.PUBLIC  })
    
    def test_delete_view(self):
        # Need to test what happens when a user is not logged in
        # when a user tries to delete a recipe to who they don't have access
        # when a user tries to delete a recipe they own (success!)
    
        test_user1 = User.objects.get(username='testuser1')
        test_user2 = User.objects.get(username='testuser2')

        created_recipe = Recipe.objects.create(recipe_name='Test Public Recipe 3',ingredients='butter,flour,cherries', recipe_tags='french,japanese', task_list='Task1;Task2;Task3', \
                visibility=Recipe.PUBLIC, user_name=test_user1)
        
        test_fetch = Recipe.objects.get(recipe_name='Test Public Recipe 3')
        self.assertEquals(test_fetch.ingredients, created_recipe.ingredients)
        self.assertEquals(test_fetch.recipe_tags, created_recipe.recipe_tags)
        self.assertEquals(test_fetch.task_list, created_recipe.task_list)
        self.assertEquals(test_fetch.id, created_recipe.id)
        
        # When a user is logged in but do not own the recipe, we redirect to the index page and display an error message
        login1 = self.client.login(username='testuser2', password='gluglu2')
        delete_url = '/recipeviewer/delete/%d/' % created_recipe.id
        response = self.client.post(delete_url)
        self.assertRedirects(response, '/recipeviewer/index')
        # messages = list(response.context['messages'])
        # self.assertEqual(len(messages),1)
        # for message in messages:
        #     self.assertTrue('You are not authorized to delete' in message)
        test_fetch = Recipe.objects.get(recipe_name='Test Public Recipe 3')
        self.assertEquals(test_fetch.id, created_recipe.id)

        self.client.logout
        response = self.client.post(delete_url)
        self.assertRedirects(response, '/recipeviewer/index')
        test_fetch = Recipe.objects.get(recipe_name='Test Public Recipe 3')
        self.assertEquals(test_fetch.id, created_recipe.id)

        login1 = self.client.login(username='testuser1', password='gluglu1')
        response = self.client.post(delete_url)
        self.assertRedirects(response, '/recipeviewer/index')
        test_fetch = Recipe.objects.filter(recipe_name='Test Public Recipe 3')
        self.assertEquals(len(test_fetch),0)        

