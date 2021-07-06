# Generated by Django 3.2.4 on 2021-07-05 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=50)),
                ('ingredients', models.TextField()),
                ('recipe_tags', models.CharField(blank=True, max_length=80, null=True)),
                ('task_list', models.TextField()),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='recipes/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('visibility', models.CharField(choices=[('PB', 'Public'), ('PV', 'Private')], default='PV', max_length=2)),
                ('user_name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.TextField()),
                ('visibility', models.CharField(choices=[('PB', 'Public'), ('PV', 'Private')], default='PV', max_length=2)),
                ('recipe_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='recipeViewer.recipe')),
                ('user_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
