from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from auth import auth, is_session_expired
from database import get_db_connection
from flask_session import Session
import random

app = Flask(__name__)

# Session Configuration
app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Register authentication blueprint
app.register_blueprint(auth, url_prefix='/auth')

# Sample Food Datasets (calories per 100g)
breakfast_items = {
    "Poha": 180, "Upma": 200, "Dosa": 168, "Idli": 120, "Paratha": 250,
    "Aloo Puri": 280, "Dhokla": 150, "Besan Chilla": 180, "Thepla": 200, "Sprouts": 100,
    "Vegetable Sandwich": 150, "Oats": 120, "Muesli": 130, "Pesarattu": 190, "Sabudana Khichdi": 230,
    "Vermicelli Upma": 180, "Chana Chaat": 150, "Methi Thepla": 220, "Ragi Dosa": 140, "Masala Oats": 160
}

lunch_items = {
    "Dal Tadka": 150, "Chana Masala": 180, "Rajma Chawal": 220, "Paneer Bhurji": 250, "Bhindi Fry": 120,
    "Baingan Bharta": 100, "Mix Veg": 120, "Palak Paneer": 180, "Matar Paneer": 200, "Aloo Gobi": 140,
    "Kaddu Sabzi": 110, "Kadhi Pakora": 160, "Dum Aloo": 180, "Vegetable Pulao": 200, "Khichdi": 180,
    "Dal Makhani": 230, "Gobi Masala": 150, "Lauki Sabzi": 90, "Sambhar": 130, "Toor Dal": 160
}

snacks_items = {
    "Bhel Puri": 150, "Dhokla": 150, "Roasted Chana": 120, "Makhana": 100, "Peanut Chaat": 180,
    "Fruit Salad": 90, "Sprouts Salad": 100, "Sundal": 110, "Chia Pudding": 120, "Roasted Fox Nuts": 80,
    "Corn Chaat": 130, "Hummus with Carrots": 140, "Masala Papad": 120, "Cucumber Sticks": 40, "Banana Shake": 180,
    "Mixed Nuts": 220, "Paneer Tikka": 250, "Yogurt with Honey": 110, "Oats Cookies": 160, "Chikki": 200
}

dinner_items = {
    "Methi Thepla": 220, "Roti with Sabzi": 180, "Khichdi": 160, "Vegetable Soup": 90, "Dal Khichdi": 170,
    "Besan Chilla": 180, "Idli with Sambhar": 140, "Lauki Sabzi": 90, "Palak Dal": 140, "Mix Veg Curry": 150,
    "Bhindi Roti": 180, "Moong Dal Chilla": 160, "Vegetable Daliya": 140, "Miso Soup": 100, "Gobi Paratha": 220,
    "Vegetable Stew": 130, "Paneer Bhurji with Roti": 210, "Cabbage Sabzi": 100, "Dal Palak": 150, "Pumpkin Soup": 110
}

def calculate_daily_calories(gender, age, weight, height, target_weight, months, activity_level):
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {"very low": 1.2, "little": 1.375, "medium": 1.55, "high": 1.725, "extreme": 1.9}
    daily_calories = bmr * activity_multipliers[activity_level]
    
    total_calories_to_lose = (weight - target_weight) * 7700  
    daily_deficit = total_calories_to_lose / (months * 30)
    target_daily_calories = daily_calories - daily_deficit

    return max(target_daily_calories, 1200)

def generate_meal_plan(daily_calories):
    meal_distribution = {"breakfast": 0.25, "lunch": 0.35, "snacks": 0.15, "dinner": 0.25}
    meal_options = {"breakfast": breakfast_items, "lunch": lunch_items, "snacks": snacks_items, "dinner": dinner_items}

    plan = []
    for _ in range(7):
        day_meals = {}
        for meal, percentage in meal_distribution.items():
            calories_needed = daily_calories * percentage
            chosen_meal = random.choice(list(meal_options[meal].keys()))
            per_100g_calories = meal_options[meal][chosen_meal]
            grams_needed = round((calories_needed / per_100g_calories) * 100, 1)
            day_meals[meal] = {"item": chosen_meal, "calories": calories_needed, "grams": grams_needed}
        plan.append(day_meals)
    
    return plan

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diet')
def diet():
    if 'user_id' not in session or is_session_expired():
        session['next'] = url_for('diet')  # Store intended destination before redirecting to login
        return redirect(url_for('auth.login'))
    return render_template('diet.html')

@app.route('/pricing')
def pricing():
    if 'user_id' not in session or is_session_expired():
        session['next'] = url_for('pricing')  # Store intended destination before redirecting to login
        return redirect(url_for('auth.login'))
    return render_template('pricing.html')

@app.route('/consult')
def consult():
    if 'user_id' not in session or is_session_expired():
        session['next'] = url_for('consult')  # Store intended destination before redirecting to login
        return redirect(url_for('auth.login'))
    return render_template('consult.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'user_id' not in session or is_session_expired():
        return jsonify({"error": "Unauthorized"}), 403  # Restrict calculation if not logged in or session expired

    data = request.json
    daily_calories = calculate_daily_calories(data['gender'], data['age'], data['weight'], data['height'], data['target_weight'], data['months'], data['activity_level'])
    meal_plan = generate_meal_plan(daily_calories)
    return jsonify({"daily_calories": daily_calories, "meal_plan": meal_plan})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
