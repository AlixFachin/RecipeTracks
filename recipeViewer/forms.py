from django import forms
from .models import Recipe, Track
from PIL import Image
from users.imagetools import image_transpose_exif

import pdb

class RecipeForm(forms.ModelForm):

    placeholders = { 'task_list' : "Write steps in the recipe separated by ';' ", 'recipe_name' : 'e.g. puff pastry' , 'recipe_tags' : 'e.g. basics, japanese, pastry, kid-friendly, ...' ,}
    
    # Variables necessary for the Picture Crop modal
    x = forms.FloatField(widget=forms.HiddenInput, required=False)
    y = forms.FloatField(widget=forms.HiddenInput, required=False)
    width = forms.FloatField(widget=forms.HiddenInput, required=False)
    height = forms.FloatField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Recipe
        fields = ['recipe_name', 'visibility', 'recipe_tags', 'image_file', 'ingredients', 'task_list',  'x','y','width', 'height',]
    
    def __init__(self, *args, **kwargs):
        #Overriding the init function so that we can set field attributes
        super(RecipeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            # field will contain a string with the name of each form field
            if self.fields[field].widget.__class__.__name__ in ('AdminTextInputWidget' , 'Textarea' ,'TextInput', 'NumberInput' , 'AdminURLFieldWidget', 'Select'): 
                self.fields[field].widget.attrs.update({ 'class': 'form-control' })
            if field in RecipeForm.placeholders:
                self.fields[field].widget.attrs.update({'placeholder' : RecipeForm.placeholders[field]})

    def save(self):
        recipe = super(RecipeForm, self).save()

        # Cropping the picture
        
        if self.cleaned_data.get('image_file') is not None and self.cleaned_data.get('image_file') != False:

            image = Image.open(recipe.image_file)
            image = image_transpose_exif(image)

            if self.cleaned_data.get('x') is not None and self.cleaned_data.get('y') is not None and self.cleaned_data.get('width') is not None and self.cleaned_data.get('height') is not None:

                x = self.cleaned_data.get('x')
                y = self.cleaned_data.get('y')
                w = self.cleaned_data.get('width')
                h = self.cleaned_data.get('height')
            else:
                # If not correct - we will aim towards the center of the picture
                image_width, image_height = image.size
                if image_width > image_height:
                    x = (image_width - image_height) / 2
                    y = 0
                    w = image_height
                    h = image_height
                else:
                    x = 0
                    y = (image_height - image_width) / 2
                    w = image_width
                    h = image_width

            cropped_image = image.crop((x,y,x+w,y+h))
            resized_image = cropped_image.resize((300,300), Image.ANTIALIAS)
            resized_image.save(recipe.image_file.path)

        return recipe

class RecipeSearchForm(forms.Form):

    name_filter = forms.CharField(label='Recipe Name', required=False)
    tags_filter = forms.CharField(label='Recipe Tags', required=False)
    ingredients_filter = forms.CharField(label='Ingredients Search', required=False)
    include_variations_in_search = forms.BooleanField(label='Include recipe variations in search result' ,required=False)

    placeholders = { 'tags_filter' : 'e.g. french,kid-friendly', 'ingredients_filter' : 'e.g. flour, mirin'  }

    def __init__(self, *args, **kwargs):
        #Overriding the init function so that we can set field attributes
        super(RecipeSearchForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            # field will contain a string with the name of each form field
            if self.fields[field].widget.__class__.__name__ in ('AdminTextInputWidget' , 'Textarea' ,'TextInput', 'NumberInput' , 'AdminURLFieldWidget', 'Select'): 
                self.fields[field].widget.attrs.update({ 'class': 'form-control' })
            if field in RecipeSearchForm.placeholders:
                self.fields[field].widget.attrs.update({'placeholder' : RecipeSearchForm.placeholders[field]})

class TrackForm(forms.ModelForm):

    class Meta:
        model = Track
        fields = ['comment', 'visibility', 'recipe_id',]
    
    def __init__(self, *args, **kwargs):
        super(TrackForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows' : 2})
        self.fields['visibility'].widget.attrs.update({'class': 'form-control'})
        self.fields['recipe_id'].widget.attrs.update({'class': 'form-control'})
        
        if 'recipe_id' in kwargs:
            # If we specify a recipe id
            self.fields['recipe_id'].widget.attrs.update({'class' : 'd-none'})
            self.fields['recipe_id'].queryset = Recipe.objects.filter(id=kwargs['recipe_id'])
    
    def restrict_recipe(self, recipe_id):
        self.fields['recipe_id'].widget.attrs.update({'class' : 'form-control d-none'})
        self.fields['recipe_id'].queryset = Recipe.objects.filter(id=recipe_id)

