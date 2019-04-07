from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/foodiesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer(), primary_key=True)
    ingredient_name = db.Column(db.String(80))
    ingredient_type = db.Column(db.String(50))
    ingredient_quantity = db.Column(db.String(50))

    def __init__(self, ingredient_id, ingredient_name, ingredient_type, ingredient_quantity):
     self.ingredient_id = ingredient_id
     self.ingredient_name = ingredient_name
     self.ingredient_type = ingredient_type
     self.ingredient_quantity = ingredient_quantity

class Cuisine(db.Model):
   cuisine_id = db.Column(db.Integer(), primary_key=True)
   cuisine_name = db.Column(db.String(50))

   def __init__(self, cuisine_id, cuisine_name):
    self.cuisine_id = cuisine_id
    self.cuisine_name = cuisine_name


class Author(db.Model):
   author_id = db.Column(db.Integer(), primary_key=True)
   first_name = db.Column(db.String(50))
   last_name = db.Column(db.String(50))

   def __init__(self, author_id, first_name, last_name):
    self.author_id = author_id
    self.first_name = first_name
    self.last_name = last_name

class Recipe(db.Model):
   recipe_id = db.Column(db.Integer(), primary_key=True)
   recipe_title = db.Column(db.String(90), unique=True)
   recipe_description = db.Column(db.String(250))
   author_id = db.Column(db.Integer, db.ForeignKey(
   'author.author_id'), nullable=False)
   ingredient_id = db.Column(db.Integer, db.ForeignKey(
   'ingredient.ingredient_id'), nullable=False)
   recipe_method = db.Column(db.String(500))
   recipe_photo = db.Column(db.String())
   recipe_date = db.Column(db.String(10))
   recipe_rating = db.Column(db.Integer())
   cuisine_id = db.Column(db.Integer, db.ForeignKey(
   'cuisine.cuisine_id'), nullable=False)

   def __init__(self, recipe_id, recipe_title, recipe_description, recipe_method, recipe_photo, recipe_date, recipe_rating):
    self.recipe_id = recipe_id
    self.recipe_title = recipe_title
    self.recipe_description = recipe_description
    self.recipe_method = recipe_method
    self.recipe_photo = recipe_photo
    self.recipe_date = recipe_date
    self.recipe_rating = recipe_rating


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addnew')
def addnew():
    return render_template('addnew.html') 

@app.route('/addnew', methods=["GET", "POST"])
def newrecipe(): 
    if request.method == "POST":
        print(request.form)
        return render_template('allrecipes.html')
       # recipe_title=request.form['recipetitle']


if __name__ == "__main__":
    manager.run()



# class Author(db.Model):
#     author_id = db.Column(db.Integer(), primary_key=True)

# class Recipe(db.Model):
#     recipe_id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(90), unique=True)
#     description = db.Column(db.Text(250))
#     author_id = db.Column(db.Integer, db.ForeignKey(
#     'author.author_id'), nullable=False)
#     ingredient_id = db.Column(db.Integer, db.ForeignKey(
#     'ingredient.ingredient_id'), nullable=False),
#     method = db.Column(db.Text(500))
#     photo = db.Column(db.Text)
#     creationdate = db.Column(db.TimeStamp)
#     rating = db.Column(db.Integer(),
#     cuisine_id = db.Column(db.Integer, db.ForeignKey(
#     'cuisine.cuisine_id'), nullable=False)


