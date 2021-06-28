from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash # Necessary when the user changes password
from django.contrib.auth.forms import PasswordChangeForm
from recipeViewer.models import Recipe, Track # Import both to be able to list all the recipes and tracks on the profile page
from django.utils import translation
from django.utils.translation import ugettext_lazy as _ 
from django.conf import settings

# Create your views here.
def register(request):
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            messages.success(request, 'Welcome {} your account is created'.format(username))
            form.save()
            return redirect('login')
        else:
            messages.error(request,str(form.errors)) 
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', { 'form' : form })

@login_required
def profilepage(request):
    # We will try to find all recipes made by this user
    user_recipes = Recipe.objects.filter(user_name=request.user.id)
    track_list = Track.objects.filter(user_id=request.user.id)
    currentProfile = Profile.objects.filter(user=request.user.id)[0]
    picture_form = ProfileForm(instance=currentProfile)

    return render(request, 'users/profile.html', {'user_recipes' : user_recipes, 'track_list' : track_list, 'picture_form' : picture_form })

def set_language_redirect(request, new_language):
    # We will set the language and redirect to the previous page
    if translation.check_for_language(new_language):
        translation.activate(new_language)
        request = redirect('home')
        request.set_cookie(settings.LANGUAGE_COOKIE_NAME, new_language)
        return request
    else:
        return redirect('home')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _ ('Your password was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the error below'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', { 'form' : form })

def change_picture(request):
    
    currentProfile = Profile.objects.filter(user=request.user.id)[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES, instance=currentProfile)
        if form.is_valid():
            # We need to open the current Profile and save
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=currentProfile)
    
    return render(request, 'users/change_profile_picture.html', {'form' : form} )