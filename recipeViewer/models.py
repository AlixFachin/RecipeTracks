from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _ 

# Create your models here.
class Recipe(models.Model):
    
    PUBLIC = 'PB'
    PRIVATE = 'PV'
    VISIBILITY_CHOICES = ((PUBLIC, _('Public')), (PRIVATE, _('Private')))
    RECIPES_PER_PAGE = 5

    recipe_name = models.CharField(max_length=50)
    ingredients = models.TextField()
    recipe_tags = models.CharField(max_length=80, null=True, blank=True)
    task_list = models.TextField()
    image_file = models.ImageField(upload_to='recipes/', null=True, blank=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='recipes')
    created_date = models.DateTimeField(editable=False, default=timezone.now)
    visibility = models.CharField(max_length=2, choices=VISIBILITY_CHOICES, default=PRIVATE)
    # Relations with other recipes
    variation_of = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='variations')

    def __str__(self):
        return self.recipe_name

    def save(self, *args, **kwargs):
        ''' On save, update timestamp '''
        if not self.id:
            self.created_date = timezone.now()
        return super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recipeViewer:detailedViewer",args=[self.pk] )

class Track(models.Model):
    PUBLIC = 'PB'
    PRIVATE = 'PV'
    VISIBILITY_CHOICES = ((PUBLIC, _('Public')), (PRIVATE, _('Private')))

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=1, related_name='tracks')
    created_date = models.DateTimeField(editable = False, default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    visibility = models.CharField(max_length=2, choices=VISIBILITY_CHOICES, default=PRIVATE)

    def __str__(self):
        return str(self.recipe_id) + "/" + str(self.user_id) + self.created_date.strftime(" - %d %m %Y")

    def save(self, *args, **kwargs):

        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        return super(Track, self).save(*args, **kwargs)
