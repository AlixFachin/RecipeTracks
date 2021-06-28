from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from PIL import Image
from .imagetools import image_transpose_exif, get_image_orientation

from django.contrib import messages

import pdb

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    
    # Variables necessary for the Picture Crop modal
    x = forms.FloatField(widget=forms.HiddenInput, required=False)
    y = forms.FloatField(widget=forms.HiddenInput, required=False)
    width = forms.FloatField(widget=forms.HiddenInput, required=False)
    height = forms.FloatField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Profile
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class':'form-control'})
    
    def save(self):
        profile = super(ProfileForm, self).save()

         # Cropping the picture
        
        if self.cleaned_data.get('image') is not None and self.cleaned_data.get('image') != False:

            image = Image.open(profile.image)
            #exif_data = image._getexif()
            
            #image = image_transpose_exif(image) # Correct the image orientation according to EXIF data in the case it was taken with a mobile phone

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
            resized_image.save(profile.image.path)

        return profile
