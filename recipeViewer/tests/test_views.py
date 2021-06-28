from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from recipeViewer.models import Recipe, Track

class test_index_view(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 20 recipes for pagination and public tests.
        # The first 15 recipes will be public, the last 5 ones will be private

        test_user1 = User.objects.create_user(username='testuser1', password='gluglu1')
        test_user2 = User.objects.create_user(username='testuser2', password='gluglu2')

        number_of_public_recipes = 15
        number_of_private_recipes = 5
        for x in range(number_of_public_recipes):
            Recipe.objects.create(recipe_name='Dummy Public Recipe %d' % x,ingredients='ingredient list %d' % x, recipe_tags='french,japanese,%d' % x, task_list='Task1;Task2;Task3', \
                visibility=Recipe.PUBLIC, user_name=test_user1)
        for x in range(number_of_private_recipes):
            Recipe.objects.create(recipe_name='Dummy Private Recipe %d' % x,ingredients='ingredient list %d' % x, recipe_tags='french,japanese,%d' % x, task_list='Task1;Task2;Task3', \
                visibility=Recipe.PRIVATE, user_name=test_user2)

    def test_view_exist_at_url_location(self):
        response = self.client.get('/recipeviewer/index')
        self.assertEquals(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('recipeViewer:index'))
        self.assertEquals(response.status_code, 200)
    
    def test_pagination_is_five(self):
        response = self.client.get(reverse('recipeViewer:index'))
        self.assertEquals(response.status_code, 200)
        #self.assertTrue('is_paginated' in response.context)
        #self.assertTrue(response.context['is_paginated'] == True)
        page_recipe_list = response.context['all_recipe_list']
        self.assertTrue(len(response.context['all_recipe_list']) == 5)
    
    # TO DO -> Need to make sure that on page 1 the recipes 1->5 are present, on page 2 recipes 6->10
    def test_proper_recipes_in_pagination(self):

        # Looking at the differences between user 1 and user 2
        login1 = self.client.login(username='testuser1', password='gluglu1')
        response = self.client.get('/recipeviewer/index?page=1')
        self.assertEquals(str(response.context['user']),'testuser1')
        recipe_paginator = response.context['all_recipe_list'].paginator
        self.assertEquals(len(recipe_paginator.page_range),3)
        # Testing the proper ids (index view should display the ids in created date decreasing)
        recipe_list = response.context['all_recipe_list']
        self.assertEquals(recipe_list[0].recipe_name,'Dummy Public Recipe 14')
        self.assertEquals(recipe_list[1].recipe_name,'Dummy Public Recipe 13')
        self.assertEquals(recipe_list[2].recipe_name,'Dummy Public Recipe 12')
        self.assertEquals(recipe_list[3].recipe_name,'Dummy Public Recipe 11')
        self.assertEquals(recipe_list[4].recipe_name,'Dummy Public Recipe 10')
        self.client.logout

        # Login with test user 2
        login1 = self.client.login(username='testuser2', password='gluglu2')
        response = self.client.get('/recipeviewer/index?page=1')
        self.assertEquals(str(response.context['user']),'testuser2')
        recipe_paginator = response.context['all_recipe_list'].paginator
        self.assertEquals(len(recipe_paginator.page_range),4)
        recipe_list = response.context['all_recipe_list']
        self.assertEquals(recipe_list[0].recipe_name,'Dummy Private Recipe 4')
        self.assertEquals(recipe_list[1].recipe_name,'Dummy Private Recipe 3')
        self.assertEquals(recipe_list[2].recipe_name,'Dummy Private Recipe 2')
        self.assertEquals(recipe_list[3].recipe_name,'Dummy Private Recipe 1')
        self.assertEquals(recipe_list[4].recipe_name,'Dummy Private Recipe 0')
        self.client.logout

class test_detailed_view(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='gluglu1')
        test_user2 = User.objects.create_user(username='testuser2', password='gluglu2')

        # We will create one recipe from user 1 (public), one recipe from user 2 (private)
        # We need to check that user1 can access recipe 1 but cannot access recipe2
        # We need to check that user2 can access recipe 2 and recipe 1

        # Then we will create comments/tracks on recipe1. One public comment by user 1 and one private comment by user 2.
        # We need to check that user 1 can see only one comment but user 2 can see two comments.

        first_recipe = Recipe.objects.create(recipe_name='Test Public Recipe 1',ingredients='butter,flour,cherries', recipe_tags='french,japanese', task_list='Task1;Task2;Task3', \
                visibility=Recipe.PUBLIC, user_name=test_user1)
        second_recipe = Recipe.objects.create(recipe_name='Test Public Recipe 2',ingredients='raisins,walnuts,peanuts', recipe_tags='mexican,vegan', task_list='Task1;Task2;Task3', \
                visibility=Recipe.PRIVATE, user_name=test_user2)
        first_track = Track.objects.create(user_id=test_user1, recipe_id=first_recipe, visibility=Track.PUBLIC, comment='This is a dummy comment 1')
        second_track = Track.objects.create(user_id=test_user2, recipe_id=first_recipe, visibility=Track.PRIVATE, comment='This is a dummy comment 2')
    
    def test_view_exist_at_url_location(self):
        login1 = self.client.login(username='testuser1', password='gluglu1')
        first_recipe = Recipe.objects.filter(recipe_name='Test Public Recipe 1')[0]
        response = self.client.get('/recipeviewer/detail/%d/' % first_recipe.id)
        self.assertEquals(response.status_code, 200)
        self.client.logout
    
    def test_view_url_accessible_by_name(self):
        login1 = self.client.login(username='testuser1', password='gluglu1')
        response = self.client.get(reverse('recipeViewer:detailedViewer', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.client.logout
    
    def test_proper_permissions_for_detail_view(self):
        # We need to check that user1 can access recipe 1 but cannot access recipe2
        # We need to check that user2 can access recipe 2 and recipe 1
        login1 = self.client.login(username='testuser1', password='gluglu1')
        response = self.client.get('/recipeviewer/detail/1/')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/recipeviewer/detail/2/')
        self.assertEquals(response.status_code, 302)
        self.client.logout

        login2 = self.client.login(username='testuser2', password='gluglu2')
        response = self.client.get('/recipeviewer/detail/1/')
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/recipeviewer/detail/2/')
        self.assertEquals(response.status_code, 200)
        self.client.logout
    
    def test_proper_visibility_of_tracks_in_detailed_view(self):
        login1 = self.client.login(username='testuser1', password='gluglu1')
        response = self.client.get('/recipeviewer/detail/1/')
        track_list = response.context['track_list']
        self.assertEquals(len(track_list),1)
        self.assertEquals(track_list[0].comment,'This is a dummy comment 1')
        self.client.logout

        login2 = self.client.login(username='testuser2', password='gluglu2')
        response = self.client.get('/recipeviewer/detail/1/')
        track_list = response.context['track_list']
        self.assertEquals(len(track_list),2)
        self.assertEquals(track_list[0].comment,'This is a dummy comment 1')
        self.client.logout

class test_search_view(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='gluglu1')
        test_user2 = User.objects.create_user(username='testuser2', password='gluglu2')
        first_recipe = Recipe.objects.create(recipe_name='Test Public Recipe 1',ingredients='butter,flour,cherries', recipe_tags='french,japanese', task_list='Task1;Task2;Task3', \
                visibility=Recipe.PUBLIC, user_name=test_user1)
        second_recipe = Recipe.objects.create(recipe_name='Test Private Recipe 2',ingredients='raisins,walnuts,peanuts', recipe_tags='mexican,vegan', task_list='Task1;Task2;Task3', \
                visibility=Recipe.PRIVATE, user_name=test_user2)
        for x in range(5):
            Recipe.objects.create(recipe_name='Recipe ABC %d' % x, ingredients='flour,cherry,butter', recipe_tags='french,pastry,basic',task_list='Task1;Task2;Task3', \
                visibility=Recipe.PRIVATE, user_name=test_user1)
        for x in range(5):
            Recipe.objects.create(recipe_name='Recipe DEF %d' % x, ingredients='butter,egg,sugar', recipe_tags='pastry,kids-friendly',task_list='Task1;Task2;Task3', \
                visibility=Recipe.PRIVATE, user_name=test_user1)
        for x in range(5):
            Recipe.objects.create(recipe_name='Recipe XYZ %d' % x, ingredients='pork,soy sauce, mirin', recipe_tags='japanese, basic',task_list='Task1;Task2;Task3', \
                visibility=Recipe.PRIVATE, user_name=test_user1)

    def test_view_exist_at_url_location(self):
        response = self.client.get('/recipeviewer/search')
        self.assertEquals(response.status_code, 200)
    
    def test_accurate_search_results(self):
        # Test 1 and 2 -> Tests that each user can access only their own recipes + the public ones
        self.client.login(username='testuser2', password='gluglu2')
        response=self.client.post('/recipeviewer/search',{'name_filter' : '', 'tags_filter': '', 'ingredients_filter': '',})
        self.assertEquals(response.status_code,200)
        self.assertEquals(len(response.context['recipe_list']),2)
        self.client.logout

        self.client.login(username='testuser1', password='gluglu1')
        response=self.client.post('/recipeviewer/search',{'name_filter' : '', 'tags_filter': '', 'ingredients_filter': '',})
        self.assertEquals(response.status_code,200)
        self.assertEquals(len(response.context['recipe_list']),16)
        # Various test of filter patterns and lengths of replies
        response=self.client.post('/recipeviewer/search',{'name_filter' : 'ABC', 'tags_filter': '', 'ingredients_filter': '',})
        self.assertEquals(len(response.context['recipe_list']),5)
        response=self.client.post('/recipeviewer/search',{'name_filter' : '', 'tags_filter': '', 'ingredients_filter': 'butter',})
        self.assertEquals(len(response.context['recipe_list']),11)
        response=self.client.post('/recipeviewer/search',{'name_filter' : '', 'tags_filter': '', 'ingredients_filter': 'butter,sugar',})
        self.assertEquals(len(response.context['recipe_list']),5)
        response=self.client.post('/recipeviewer/search',{'name_filter' : '', 'tags_filter': 'french', 'ingredients_filter': '',})
        self.assertEquals(len(response.context['recipe_list']),6)
        response=self.client.post('/recipeviewer/search',{'name_filter' : '', 'tags_filter': 'french,pastry', 'ingredients_filter': '',})
        self.assertEquals(len(response.context['recipe_list']),5)

class test_recipe_crud_views(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='gluglu1')
        test_user2 = User.objects.create_user(username='testuser2', password='gluglu2')

    def test_create_view(self):
        # 1. Test of GET use the right address
        # 2. Test of GET to use the right template
        # 3. Test of POST to create a new recipe
        # 4. Test that after creation all the fields are set to the expected values
        pass

    def test_update_view(self):
        # 1. Test of GET to use the proper address
        # 2 Test of GET to use the proper template
        # 3 Test of return 404 page if looking for a recipe which doesn't exist
        # 4 Test of error message for user trying to edit a recipe they don't own.
        # 5 Test of updating most values through the views and test that the fields are properly edited afterwards
        pass

    def test_delete_view(self):
        # 1 test of proper address 
        # 2 test if the user doesn't own the recipe
        # 3 test that if the user owns the recipe, that the recipe is properly destroyed.
        pass

