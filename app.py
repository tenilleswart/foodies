from flask import Flask, request, render_template, redirect,  url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.utils import secure_filename
from flask_paginate import Pagination, get_page_parameter
from flask import Blueprint, abort
from sqlalchemy.sql.expression import or_

import os
import datetime
import random
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/foodiesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='secretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

ERR_NO_FILE_SPECIFIED='error: no file specified'
IMAGE_DIRECTORY='static/images'
PER_PAGE= 6

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer(), primary_key=True)
    ingredient_name = db.Column(db.String())
    
    def __init__(self, ingredient_name):
     self.ingredient_name = ingredient_name

class Cuisine(db.Model):
   __tablename__ = 'cuisine'

   cuisine_id = db.Column(db.Integer(), primary_key=True)
   cuisine_name = db.Column(db.String())

   def __init__(self, cuisine_name):
    self.cuisine_name = cuisine_name


class Author(db.Model):
   __tablename__ = 'author'

   author_id = db.Column(db.Integer(), primary_key=True)
   first_name = db.Column(db.String())
   last_name = db.Column(db.String())

   def __init__(self, first_name, last_name):
    self.first_name = first_name
    self.last_name = last_name

class Recipe(db.Model):
   __tablename__ = 'recipe'

   recipe_id = db.Column(db.Integer(), primary_key=True)
   recipe_title = db.Column(db.String(), unique=True)
   recipe_description = db.Column(db.String())
   author_id = db.Column(db.Integer, db.ForeignKey(
   'author.author_id'), nullable=False)
   ingredient_id = db.Column(db.Integer, db.ForeignKey(
   'ingredient.ingredient_id'), nullable=False)
   recipe_method = db.Column(db.String())
   recipe_photo = db.Column(db.String())
   recipe_date = db.Column(db.Date, default=datetime.datetime.utcnow)
   recipe_rating = db.Column(db.Integer())
   cuisine_id = db.Column(db.Integer, db.ForeignKey(
   'cuisine.cuisine_id'), nullable=False)

   def __init__(self, recipe_title, recipe_description, recipe_method, author_id, ingredient_id, cuisine_id, recipe_photo, recipe_rating):
    self.recipe_title = recipe_title
    self.recipe_description = recipe_description
    self.recipe_method = recipe_method
    self.author_id = author_id
    self.ingredient_id = ingredient_id
    self.cuisine_id = cuisine_id
    self.recipe_photo = recipe_photo
    self.recipe_rating = recipe_rating

db.create_all()
db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addnew')
def addnew():
    return render_template('addnew.html') 

def get_results(offset, per_page, results):
    return results[offset: offset + per_page]

@app.route('/allrecipes')
def allrecipes():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    results = []
    results = db.session.query(Recipe, Author, Ingredient, Cuisine).join(
        Author).join(Ingredient).join(Cuisine).all()
    print(results)
    page_size = len(results)
    offset = (page - 1) * PER_PAGE

    pagination_results = get_results(offset, PER_PAGE, results)
  
    pagination = Pagination(page=page, per_page=PER_PAGE,
                            total=page_size, css_framework='bootstrap3')

    return render_template('allrecipes.html', results=pagination_results, page=page,
                           per_page=PER_PAGE, pagination=pagination)
    
@app.route('/topchef')
def topchef():
    return render_template('topchef.html') 

   


def get_single_recipe(recipeId):
    single_recipe = db.session.query(Recipe, Author, Cuisine, Ingredient
                                     ).filter(Recipe.recipe_id == recipeId
                                              ).join(Author, Recipe.author_id == Author.author_id
                                                     ).join(Cuisine, Recipe.cuisine_id == Cuisine.cuisine_id
                                                            ).join(Ingredient, Recipe.ingredient_id == Ingredient.ingredient_id
                                                                   ).first()
    return single_recipe

@app.route('/allrecipes/<recipe_id>')
def recipe(recipe_id):
    result=get_single_recipe(recipe_id)
    return render_template('recipe.html', result=result)   
    
def randstr():
    '''' create random string of alpha numeric characters '''
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
@app.route('/addnew', methods=["GET", "POST"])
def newrecipe(): 
    if request.method == "POST":
        print(request.form)

        imagefile = request.files['file']
 
        if imagefile.filename == '':
          return ERR_NO_FILE_SPECIFIED

        safefilename=secure_filename(randstr() + '-' + imagefile.filename)
        imagepath='{}/{}'.format(IMAGE_DIRECTORY, safefilename)


        first_name_request = request.form['authorfirstname']
        last_name_request = request.form['authorlastname']
        authorObject = Author(first_name = first_name_request, last_name = last_name_request)
        db.session.add(authorObject)
        db.session.commit()


        ingredient_name_request =request.form['ingredients']
        ingredientObject = Ingredient(ingredient_name = ingredient_name_request)
        db.session.add(ingredientObject)
        db.session.commit()

        cuisine_name_request =request.form['cuisine']
        cuisineObject = Cuisine(cuisine_name = cuisine_name_request)
        db.session.add(cuisineObject)
        db.session.commit()


        recipe_title_request = request.form['recipetitle']
        recipe_photo_request = safefilename
        recipe_description_request =  request.form['description']
        recipe_method_request = request.form['method']
        recipe_rating_request = request.form['rating-input-1']

        print(recipe_rating_request)
        
        recipeObject = Recipe(recipe_title=recipe_title_request,
          recipe_description=recipe_method_request,
          author_id=authorObject.author_id,
          ingredient_id=ingredientObject.ingredient_id,
          recipe_method=recipe_method_request,
          recipe_photo=recipe_photo_request,
          recipe_rating=recipe_rating_request,
          cuisine_id=cuisineObject.cuisine_id)
         
        
        imagefile.save(imagepath)
        db.session.add(recipeObject)
        db.session.commit()
  
        flash('Your Recipe is now Live!')
        result=get_single_recipe(recipeObject.recipe_id)
        return render_template('recipe.html',result=result)
    


if __name__ == "__main__":
    manager.run()




