from database import db
from datetime import datetime

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    servings = db.Column(db.Integer)
    thumbnail_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade='all, delete-orphan')
    instructions = db.relationship('Instruction', backref='recipe', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Recipe {self.name}>'

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(100))
    unit = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'

class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<Instruction Step {self.step_number}>'

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(50))  # breakfast, lunch, dinner, snack
    
    recipe = db.relationship('Recipe', backref='meal_plans')
    
    def __repr__(self):
        return f'<MealPlan {self.date} - {self.meal_type}>'

class GroceryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.Column(db.Text)  # JSON string of grocery items
    
    def __repr__(self):
        return f'<GroceryList {self.created_at}>'
