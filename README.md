# Cookbook Web App

A Flask-based web application for managing recipes, planning meals, and generating grocery lists.

## Features

- **Add Recipes**: Manually enter recipes or automatically import from URLs
- **View & Edit Recipes**: Browse, search, edit, and delete your recipe collection
- **Meal Calendar**: Plan meals by day (breakfast, lunch, dinner) on an interactive monthly calendar
- **Grocery List Generator**: Select recipes and automatically generate shopping lists with ingredient aggregation
- **Weekly Dashboard**: View current week's meals and latest grocery list on the homepage

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

## Tech Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 3.1.1
- **Database**: SQLite
- **Recipe Parsing**: recipe-scrapers 14.52.0
- **Frontend**: HTML, CSS, JavaScript

## Usage

- **Homepage**: View this week's meal plan and latest grocery list
- **Add Recipes**: Use manual entry or paste a recipe URL for automatic parsing
- **Calendar**: Click on meal slots to assign recipes, use + button to send week's recipes to grocery page
- **Groceries**: Search for recipes, adjust quantities with +/- buttons, mark items you already have, and generate your shopping list

## Network Access

The app binds to `0.0.0.0` by default, making it accessible from other devices on your local network at `http://<your-ip>:5000`.
