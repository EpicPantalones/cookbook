from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cookbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from database import db
db.init_app(app)

# Import models after db is initialized
from models import Recipe, Ingredient, Instruction, MealPlan, GroceryList

def parse_ingredient(ingredient_string):
    """Parse an ingredient string into quantity, unit, and name"""
    ingredient_string = ingredient_string.strip()
    
    # Common units to look for
    units = [
        'cup', 'cups', 'tablespoon', 'tablespoons', 'tbsp', 'tsp', 'teaspoon', 'teaspoons',
        'ounce', 'ounces', 'oz', 'fluid ounce', 'fluid ounces', 'fl oz',
        'pound', 'pounds', 'lb', 'lbs', 'gram', 'grams', 'g',
        'kilogram', 'kilograms', 'kg', 'milliliter', 'milliliters', 'ml',
        'liter', 'liters', 'l', 'pint', 'pints', 'quart', 'quarts',
        'gallon', 'gallons', 'can', 'cans', 'package', 'packages', 'pkg',
        'piece', 'pieces', 'clove', 'cloves', 'pinch', 'pinches',
        'dash', 'dashes', 'whole'
    ]
    
    # Pattern to match fractions and decimals
    # Matches: "1", "1.5", "1/2", "1 1/2", etc.
    quantity_pattern = r'^(\d+(?:\.\d+)?(?:\s*/\s*\d+)?(?:\s+\d+/\d+)?)'
    
    match = re.match(quantity_pattern, ingredient_string)
    
    if match:
        quantity_str = match.group(1).strip()
        remaining = ingredient_string[len(match.group(0)):].strip()
        
        # Evaluate fraction if present
        try:
            if '/' in quantity_str:
                # Handle mixed fractions like "1 1/2"
                parts = quantity_str.split()
                if len(parts) == 2:
                    whole = float(parts[0])
                    frac_parts = parts[1].split('/')
                    quantity = whole + (float(frac_parts[0]) / float(frac_parts[1]))
                else:
                    # Simple fraction like "1/2"
                    frac_parts = quantity_str.split('/')
                    quantity = float(frac_parts[0]) / float(frac_parts[1])
            else:
                quantity = float(quantity_str)
            
            # Round to 2 decimal places
            quantity = round(quantity, 2)
        except:
            quantity = quantity_str
        
        # Look for unit at the beginning of remaining string
        unit = 'unit'  # Default to 'unit' if not found
        name = remaining
        
        for u in units:
            # Check if remaining starts with this unit (case insensitive)
            pattern = r'^' + re.escape(u) + r'\b'
            if re.match(pattern, remaining, re.IGNORECASE):
                unit = u.lower()
                name = remaining[len(u):].strip()
                # Normalize unit names
                if unit in ['cups', 'cup']:
                    unit = 'cup'
                elif unit in ['tablespoons', 'tablespoon', 'tbsp']:
                    unit = 'tablespoon'
                elif unit in ['teaspoons', 'teaspoon', 'tsp']:
                    unit = 'teaspoon'
                elif unit in ['ounces', 'ounce', 'oz']:
                    unit = 'ounce'
                elif unit in ['pounds', 'pound', 'lb', 'lbs']:
                    unit = 'pound'
                elif unit in ['grams', 'gram', 'g']:
                    unit = 'gram'
                elif unit in ['kilograms', 'kilogram', 'kg']:
                    unit = 'kilogram'
                elif unit in ['milliliters', 'milliliter', 'ml']:
                    unit = 'milliliter'
                elif unit in ['liters', 'liter', 'l']:
                    unit = 'liter'
                elif unit in ['cans', 'can']:
                    unit = 'can'
                elif unit in ['packages', 'package', 'pkg']:
                    unit = 'package'
                elif unit in ['pieces', 'piece']:
                    unit = 'piece'
                elif unit in ['cloves', 'clove']:
                    unit = 'clove'
                elif unit in ['pinches', 'pinch']:
                    unit = 'pinch'
                elif unit in ['dashes', 'dash']:
                    unit = 'dash'
                break
        
        return {
            'quantity': quantity,
            'unit': unit,
            'name': name if name else remaining
        }
    else:
        # No quantity found, treat entire string as name
        return {
            'quantity': '',
            'unit': 'unit',
            'name': ingredient_string
        }

# Routes
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/groceries')
def groceries():
    return render_template('groceries.html')

@app.route('/add-recipes', methods=['GET', 'POST'])
def add_recipes():
    if request.method == 'POST':
        # Get basic recipe info
        name = request.form.get('name')
        description = request.form.get('description')
        prep_time = request.form.get('prep_time')
        cook_time = request.form.get('cook_time')
        servings = request.form.get('servings')
        thumbnail_url = request.form.get('thumbnail_url')
        
        # Check if recipe with same name exists
        existing_recipe = Recipe.query.filter_by(name=name).first()
        recipe_id = request.form.get('recipe_id')  # Will be set if editing
        
        if existing_recipe and (not recipe_id or str(existing_recipe.id) != recipe_id):
            # Recipe exists and we're not editing it
            return jsonify({
                'success': False,
                'error': 'duplicate',
                'message': f'A recipe named "{name}" already exists. Please use a different name or edit the existing recipe.'
            }), 409
        
        if recipe_id:
            # Edit existing recipe
            recipe = Recipe.query.get(int(recipe_id))
            if recipe:
                recipe.name = name
                recipe.description = description
                recipe.prep_time = int(prep_time) if prep_time else None
                recipe.cook_time = int(cook_time) if cook_time else None
                recipe.servings = int(servings) if servings else None
                recipe.thumbnail_url = thumbnail_url
                
                # Delete old ingredients and instructions
                Ingredient.query.filter_by(recipe_id=recipe.id).delete()
                Instruction.query.filter_by(recipe_id=recipe.id).delete()
            else:
                return jsonify({'success': False, 'error': 'Recipe not found'}), 404
        else:
            # Create new recipe
            recipe = Recipe(
                name=name,
                description=description,
                prep_time=int(prep_time) if prep_time else None,
                cook_time=int(cook_time) if cook_time else None,
                servings=int(servings) if servings else None,
                thumbnail_url=thumbnail_url
            )
            
            db.session.add(recipe)
        
        db.session.flush()  # Get the recipe ID
        
        # Add ingredients
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_quantities = request.form.getlist('ingredient_quantity[]')
        ingredient_units = request.form.getlist('ingredient_unit[]')
        
        for i in range(len(ingredient_names)):
            if ingredient_names[i]:  # Only add if name is not empty
                ingredient = Ingredient(
                    recipe_id=recipe.id,
                    name=ingredient_names[i],
                    quantity=ingredient_quantities[i] if i < len(ingredient_quantities) else '',
                    unit=ingredient_units[i] if i < len(ingredient_units) else 'unit'
                )
                db.session.add(ingredient)
        
        # Add instructions
        instructions_text = request.form.get('instructions')
        if instructions_text:
            instruction = Instruction(
                recipe_id=recipe.id,
                step_number=1,
                description=instructions_text
            )
            db.session.add(instruction)
        
        # Handle thumbnail upload
        if 'thumbnail' in request.files:
            file = request.files['thumbnail']
            if file and file.filename:
                # Save file logic here
                pass
        
        db.session.commit()
        return redirect(url_for('view_recipes'))
    
    # GET request - check if editing
    edit_id = request.args.get('edit')
    recipe_data = None
    if edit_id:
        recipe = Recipe.query.get(int(edit_id))
        if recipe:
            recipe_data = {
                'id': recipe.id,
                'name': recipe.name,
                'description': recipe.description,
                'prep_time': recipe.prep_time,
                'cook_time': recipe.cook_time,
                'servings': recipe.servings,
                'thumbnail_url': recipe.thumbnail_url,
                'ingredients': [
                    {
                        'name': ing.name,
                        'quantity': ing.quantity,
                        'unit': ing.unit
                    } for ing in recipe.ingredients
                ],
                'instructions': recipe.instructions[0].description if recipe.instructions else ''
            }
    
    return render_template('add_recipes.html', recipe=recipe_data)

@app.route('/view-recipes')
def view_recipes():
    recipes = db.session.execute(db.select(Recipe).order_by(Recipe.created_at.desc())).scalars().all()
    return render_template('view_recipes.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>', methods=['GET', 'DELETE'])
def get_recipe(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    
    if request.method == 'DELETE':
        # Delete the recipe
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Recipe deleted successfully'})
    
    # GET request - return recipe data
    
    recipe_data = {
        'id': recipe.id,
        'name': recipe.name,
        'description': recipe.description,
        'prep_time': recipe.prep_time,
        'cook_time': recipe.cook_time,
        'servings': recipe.servings,
        'thumbnail_url': recipe.thumbnail_url,
        'ingredients': [
            {
                'name': ing.name,
                'quantity': ing.quantity,
                'unit': ing.unit
            } for ing in recipe.ingredients
        ],
        'instructions': [
            {
                'step_number': inst.step_number,
                'description': inst.description
            } for inst in recipe.instructions
        ]
    }
    
    return jsonify(recipe_data)

@app.route('/parse-recipe', methods=['POST'])
def parse_recipe():
    """Parse a recipe from a URL"""
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    try:
        # Import recipe-scrapers library
        from recipe_scrapers import scrape_me
        
        scraper = scrape_me(url)
        
        # Helper function to safely extract data
        def safe_get(method, default=None):
            try:
                return method()
            except:
                return default
        
        # Extract servings number from string like "20 servings" or "4-6 servings"
        servings_raw = safe_get(scraper.yields)
        servings = None
        if servings_raw:
            # Try to extract first number from the servings string
            import re
            match = re.search(r'\d+', str(servings_raw))
            if match:
                servings = int(match.group())
        
        # Extract recipe data - each field is optional
        recipe_data = {
            'name': safe_get(scraper.title, 'Untitled Recipe'),
            'description': safe_get(scraper.host, ''),
            'prep_time': safe_get(scraper.prep_time),
            'cook_time': safe_get(scraper.cook_time),
            'servings': servings,
            'instructions': safe_get(scraper.instructions, ''),
            'thumbnail_url': safe_get(scraper.image),
            'ingredients': []
        }
        
        # Parse ingredients
        ingredients_list = safe_get(scraper.ingredients, [])
        for ingredient in ingredients_list:
            parsed = parse_ingredient(ingredient)
            recipe_data['ingredients'].append(parsed)
        
        return jsonify({'success': True, 'recipe': recipe_data})
        
    except ImportError:
        return jsonify({
            'success': False, 
            'error': 'Recipe scraping library not installed. Please install recipe-scrapers: pip install recipe-scrapers'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API Routes for Calendar
@app.route('/api/recipes')
def api_recipes():
    recipes = Recipe.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'prep_time': r.prep_time,
        'servings': r.servings,
        'thumbnail_url': r.thumbnail_url
    } for r in recipes])

@app.route('/api/recipes-with-ingredients')
def api_recipes_with_ingredients():
    recipes = Recipe.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'prep_time': r.prep_time,
        'servings': r.servings,
        'thumbnail_url': r.thumbnail_url,
        'ingredients': [{
            'name': ing.name,
            'quantity': ing.quantity,
            'unit': ing.unit
        } for ing in r.ingredients]
    } for r in recipes])

@app.route('/api/meal-plans/<int:year>/<int:month>')
def api_meal_plans(year, month):
    from datetime import date
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    plans = MealPlan.query.filter(
        MealPlan.date >= start_date,
        MealPlan.date < end_date
    ).all()
    
    return jsonify([{
        'id': p.id,
        'date': p.date.strftime('%Y-%m-%d'),
        'meal_type': p.meal_type,
        'recipe_id': p.recipe_id,
        'recipe_name': p.recipe.name if p.recipe else None
    } for p in plans])

@app.route('/api/meal-plans', methods=['POST'])
def api_create_meal_plan():
    from datetime import datetime
    data = request.get_json()
    
    date_str = data.get('date')
    meal_type = data.get('meal_type')
    recipe_id = data.get('recipe_id')
    
    # Parse date
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Check if meal plan already exists
    existing = MealPlan.query.filter_by(
        date=date_obj,
        meal_type=meal_type
    ).first()
    
    if existing:
        # Update existing
        existing.recipe_id = recipe_id
        meal_plan = existing
    else:
        # Create new
        meal_plan = MealPlan(
            date=date_obj,
            meal_type=meal_type,
            recipe_id=recipe_id
        )
        db.session.add(meal_plan)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'meal_plan_id': meal_plan.id
    })

@app.route('/api/meal-plans/<int:plan_id>', methods=['DELETE'])
def api_delete_meal_plan(plan_id):
    meal_plan = MealPlan.query.get(plan_id)
    if (meal_plan):
        db.session.delete(meal_plan)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Meal plan not found'}), 404

@app.route('/api/grocery-list', methods=['POST'])
def api_save_grocery_list():
    data = request.get_json()
    items = data.get('items', [])
    
    import json
    grocery_list = GroceryList(items=json.dumps(items))
    db.session.add(grocery_list)
    db.session.commit()
    
    return jsonify({'success': True, 'id': grocery_list.id})

@app.route('/api/grocery-list/latest', methods=['GET'])
def api_get_latest_grocery_list():
    grocery_list = GroceryList.query.order_by(GroceryList.created_at.desc()).first()
    if grocery_list:
        import json
        return jsonify({
            'success': True,
            'items': json.loads(grocery_list.items),
            'created_at': grocery_list.created_at.isoformat()
        })
    return jsonify({'success': False, 'items': []})

@app.route('/api/current-week-meals', methods=['GET'])
def api_current_week_meals():
    from datetime import date, timedelta
    today = date.today()
    # Get start of week (Sunday)
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)
    end_of_week = start_of_week + timedelta(days=6)
    
    plans = MealPlan.query.filter(
        MealPlan.date >= start_of_week,
        MealPlan.date <= end_of_week
    ).all()
    
    result = []
    for plan in plans:
        result.append({
            'date': plan.date.isoformat(),
            'meal_type': plan.meal_type,
            'recipe_id': plan.recipe_id,
            'recipe_name': plan.recipe.name if plan.recipe else None
        })
    
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
