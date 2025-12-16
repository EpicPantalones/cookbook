# Cookbook Web App

A Flask-based web application for managing recipes, planning meals, and generating grocery lists with a beautiful theme system.

## Features

- **Recipe Management**: 
  - Manually enter recipes with ingredients and instructions
  - Automatically import recipes from URLs using smart parsing
  - View, search, edit, and delete your recipe collection
  
- **Meal Planning Calendar**: 
  - Interactive monthly calendar for planning meals
  - Assign recipes to breakfast, lunch, and dinner slots
  - View your meal plan at a glance
  - Quick access to send week's recipes to grocery list
  
- **Smart Grocery Lists**: 
  - Select recipes and automatically aggregate ingredients
  - Adjust serving sizes with +/- buttons
  - Mark items you already have to exclude from the list
  - Generate consolidated shopping lists with combined quantities
  
- **Weekly Dashboard**: 
  - View current week's meal plan at a glance
  - Quick access to latest grocery list
  - Add individual grocery items directly from homepage
  
- **Theme System**:
  - Light mode (default)
  - Dark mode
  - Base2Tone Lavender Light
  - Base2Tone Lavender Dark
  - Theme preference persists across sessions

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage Flow

### Getting Started: Adding Your First Recipes

**Option 1: Manual Entry**
1. Navigate to **Add Recipes** page
2. Click the **Manual Entry** tab
3. Fill in recipe details:
   - Name, description, prep/cook time, servings
   - Add ingredients one by one (name, quantity, unit)
   - Add step-by-step instructions
4. Click **Save Recipe to Database**

**Option 2: URL Import (Automatic)**
1. Navigate to **Add Recipes** page
2. Stay on the **From URL** tab
3. Paste a recipe URL (e.g., from AllRecipes, Food Network, etc.)
4. Click **Parse Recipe**
5. Review the parsed recipe preview
6. Click **Save Recipe to Database** or **Edit Recipe** to modify first

**Pro Tip**: Build a collection of 10-15 recipes to get started!

### Planning Your Week: Using the Calendar

1. Navigate to **Calendar** page
2. Use the ◀ ▶ buttons to navigate to your desired month
3. Click on any day to expand it
4. For each meal slot (Breakfast, Lunch, Dinner):
   - Click the meal slot to open the recipe picker
   - Search for recipes using the search bar
   - Click a recipe to assign it to that meal
   - Or click "No Recipe (skip this meal)" for empty slots
5. The calendar shows meal previews on each day
6. Your meal plan is automatically saved

**Sending to Groceries**: 
- Click the **+** button next to any week number to send that entire week's recipes to the grocery page

### Creating Your Grocery List

**Method 1: From Calendar**
1. On the **Calendar** page, click the **+** button next to a week number
2. Automatically switches to **Groceries** page with the week's recipes loaded

**Method 2: Manual Selection**
1. Navigate to **Groceries** page
2. Use the search bar to find recipes
3. Click recipes from the dropdown to add them
4. Added recipes appear as colored tags

**Adjusting Your List**:
1. For each recipe, adjust quantities:
   - Use **-** button to reduce servings
   - Use **+** button to increase servings
   - Default is the recipe's original serving size
2. Click the **×** on recipe tags to remove recipes
3. Mark items you already have:
   - Enter quantity in the "Have" column
   - The system automatically subtracts from the total needed

**Generating the Final List**:
1. Click **Generate Grocery List** button
2. Review your consolidated shopping list
3. Click **Copy List** to copy to clipboard
4. Take it with you to the store!

### Using the Homepage Dashboard

The **Homepage** serves as your command center:

**This Week's Meals**:
- View the current week's meal plan (7 days)
- Each day shows all assigned meals
- Click on days to quickly see what's planned

**Latest Grocery List**:
- View your most recently generated grocery list
- See all items with combined quantities
- Check items off as you shop (checkbox functionality)

**Quick Add Items**:
- Add individual grocery items directly from the homepage
- Perfect for non-recipe items (milk, eggs, snacks, etc.)
- Items appear in your grocery list immediately

### Switching Themes

1. Click the **🎨** button in the top navigation bar
2. Select from four themes:
   - **Light**: Clean, bright interface
   - **Dark**: Easy on the eyes for night use
   - **Lavender Light**: Soft, purple-tinted theme
   - **Lavender Dark**: Muted dark theme with lavender accents
3. Your theme choice is saved and persists across all pages and sessions

## Tech Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 3.1.1
- **Database**: SQLite
- **Recipe Parsing**: recipe-scrapers 14.52.0
- **Frontend**: HTML, CSS (CSS Variables for theming), JavaScript

## Network Access

The app binds to `0.0.0.0` by default, making it accessible from other devices on your local network at `http://<your-ip>:5000`.

## Tips & Tricks

- **Meal Planning**: Plan meals on Sunday for the week ahead
- **Batch Cooking**: Select multiple recipes with similar ingredients to save money
- **Leftovers**: Adjust serving sizes up and plan leftover meals for busy days
- **Theme Switching**: Use dark themes in the evening to reduce eye strain
- **Mobile Access**: Access from your phone while shopping using the local network URL
