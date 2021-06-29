# RecipeTracks 🍰 🐟🐮

<img src="./RecipeTrack_screenshot.png" alt="app screenshot" width="400px">

## Summary 🧑‍🏫
Website based on Django which allows users to store their own set of recipes, and to record their previous experimentations and notes.

More than a recipe database, this website app is made to keep track of the users experiments as a tool to actually improve one's cooking skills. Recipes should be flexible, according to one's taste and hardware (I am pretty sure that my oven cooks pound cakes in a different time than most of the other ones). Keeping track of all those experiments is the equivalent of handwritten notes on old recipe books!

## Seeing it live! 👍
The app is currently deployed at [Python Anywhere](http://afachin.pythonanywhere.com)

## Features 🛠️
* [User authentication](https://docs.djangoproject.com/en/3.2/topics/auth/) via Django
* Saving recipes in the database with `sqllite` DB
* Users are able to add a "track" to a recipe, which is a personal annotation to the recipe. (For example: I tried to bake the cake 45 minutes but it was too little, I want to try 55 minutes next time). [As an aside, this feedback loop is essential to mastering any skill, cooking being one of them]
* Multi-lingual website thanks to the [i18n](https://docs.djangoproject.com/en/3.2/topics/i18n/) django package

## Tech used 🛠️
* The website uses [Django]() as a framework, and obviously **Python** as a language
* Django templates are "beautified" using [Bootstrap](https://getbootstrap.com/)

## How to install it locally
**Django** is a **Python**-based framework, so you need to actually install Python properly on your machine.
1. Create a virtual environment for this project

_Virtual environments_ are used in Python to isolate a project and have a set of libraries running just for this project. This enable you to have a certain version of Django installed for this RecipeTracker project, and another version somewhere else for another project.

In the project folder, please run:
```
python3 -m venv ./venv
```
This will create a `venv` folder which will contain all the libraries required for this project

2. Activate the virtual environment

Then you need to _activate_ the virtual environment, which means:
```
source ./venv/bin/activate
```
(The line above works on a Mac and on UNIX - if you have a Windows machine the actual executable depends on the shell you are using.)
Once you have activated the virtual environment, `(venv)` should be displayed at the beginning of your command prompt.

3. Install dependencies

Now you can install plenty of libraries, you won't modify your global environment on this machine.
```
python3 -m pip install -r ./requirements.txt
```

> Note: As time of writing, the `Pillow` library was not able to be installed/compiled
> on Apple M1 machines. Please refer to <https://github.com/python-pillow/Pillow/issues/5093> 
> for an explanation of how to solve this issue.)


4. Run the migrations on the database

Now you have an empty database. You need to create the proper tables for the app to be ran.
From the project root folder, type

```
python3 manage.py migrate
```

5. Run the server!

Now you should be able to run the server locally.
```
python3 manage.py runserver
```
And if everything is OK, you should see the message:

