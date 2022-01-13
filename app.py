import datetime
import os
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import sqlalchemy

load_dotenv()

app = Flask(__name__)
CORS(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import jwt

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
import models
models.db.init_app(app)


def root():
  return 'ok'
app.route('/', methods=["GET"])(root)

def create_user():
  hashed_pw = bcrypt.generate_password_hash(request.json["password"]).decode('utf-8')
  try:
    user = models.User(
      first=request.json["first"],
      last=request.json["last"],
      email=request.json["email"],
      # password=request.json["password"]
      password=hashed_pw
    )
    models.db.session.add(user)
    models.db.session.commit()
    encrypted_id = jwt.encode({"user_id": user.id}, os.environ.get('JWT_SECRET'), algorithm="HS256")
    return {
      "user": user.to_json(), 
      "user_id": encrypted_id
    }
  except sqlalchemy.exc.IntegrityError:
    return { "message": "Email must be present and unique"}, 400
app.route('/users', methods=["POST"])(create_user)

def login():
  user = models.User.query.filter_by(email=request.json["email"]).first()
  if not user:
    return {
      "message": "User not found" 
    }, 404
  # if user.password == request.json["password"]:
  if bcrypt.check_password_hash(user.password, request.json["password"]):
    encrypted_id = jwt.encode({"user_id": user.id}, os.environ.get('JWT_SECRET'), algorithm="HS256")
    return {
      "user": user.to_json(),
      "user_id": encrypted_id
    }
  else:
    return {
      "message": "login failed"
    }, 401
app.route('/users/login', methods=["POST"])(login)

def verify_user():
  # print(request.headers)
  decrypted_id = jwt.decode(request.headers['Authorization'], os.environ.get("JWT_SECRET"), algorithms=["HS256"])["user_id"]
  # user = models.User.query.filter_by(id=request.headers["Authorization"]).first() #How to look user up? We can't do it by request.json in python
  user = models.User.query.filter_by(id= decrypted_id).first()
  # if not user: 
  #   return {
  #     "message": "user not found"
  #   }, 404

  if user:
    return { "user": user.to_json()}
  else: 
    return { "message": "user not found "}, 404
  print(user)
  # return 'ok'
  return {
    "user": user.to_json()
  }
app.route('/users/verify', methods=["GET"])(verify_user)


def index():
    meals = models.Meal.query.order_by(models.Meal.date.desc()).all()

    Meal_dates = []

    for meal in Meals:
        proteins = 0
        carbohydrates = 0
        fats = 0
        calories = 0

        for food in meal.foods:
            proteins += food.proteins
            carbohydrates += food.carbohydrates 
            fats += food.fats
            calories += food.calories

        meal_dates.append({
            'meal_date' : meal,
            'proteins' : proteins,
            'carbohydrates' : carbohydrates,
            'fats' : fats,
            'calories' : calories
        })
        
app.route('/', methods=["GET", "POST"])(index)

def create_meal():
    date = request.form.get('date')

    meal = models.Meal(date=datetime.strptime(date, '%Y-%m-%d'))

    models.db.session.add(meal)
    models.db.session.commit()

app.route('/meal', methods=["POST"])(create_meal)

def add():
    nutritions = models.Nutrition.query.all()

app.route('/meal', methods=["GET"])(add)

def add_post():
    food_name = request.form.get('food-name')
    proteins = request.form.get('protein')
    carbohydrates = request.form.get('carbohydrates')
    fats = request.form.get('fat')

    nutrition_id = request.form.get('nutrition-id')

    if nutrition_id:
        nutrition = models.Nutrition.query.get_or_404(nutrition_id)
        nutrition.name = food_name
        nutrition.proteins = proteins
        nutrition.carbohydrates = carbohydrates
        nutrition.fats = fats

    else:
        new_food = models.Nutrition(
            name=food_name,
            proteins=proteins, 
            carbohydrates=carbohydrates, 
            fats=fats
        )
    
        models.db.session.add(new_nutrition)

    models.db.session.commit()

app.route('/meal', methods=["POST"])(add_post)

def delete_nutrition(nutrition_id):
    nutrition = models.Nutrition.query.get_or_404(nutrition_id)
    models.db.session.delete(nutrition)
    models.db.session.commit()

app.route('/delete_nutrition/<int:nutrition_id>', methods=["POST"])(delete_nutrition)

def edit_nutrition(nutrition_id):
    nutrition = models.Nutrition.query.get_or_404(nutrition_id)
    nutritions = models.Nutrition.query.all()

app.route('/edit_nutrition/<int:nutrition_id>', methods=["POST"])(edit_nutrition)

def view(meal_id):
    meal = models.Meal.query.get_or_404(Meal_id)

    Meals = models.Meal.query.all()

    totals = {
        'protein' : 0,
        'carbohydrates' : 0,
        'fat' : 0,
        'calories' : 0
    }

    for nutrition in meal.foods:
        totals['protein'] += nutrition.proteins
        totals['carbohydrates'] += nutrition.carbohydrates
        totals['fat'] += nutrition.fats 
        totals['calories'] += nutrition.calories

app.route('/view/<int:meal_id>', methods=["GET"])(view)

def add_nutrition_to_meal(meal_id):
    meal = models.Meal.query.get_or_404(meal_id)

    selected_nutrition = request.form.get('nutrition-select')

    nutrition = models.Nutrition.query.get(int(selected_nutrition))

    meal.nutritions.append(nutrition)
    models.db.session.commit()

app.route('/add_nutrition_to_meal/<int:meal_id>', methods=["POST"])(add_nutrition_to_meal)


def remove_nutrition_from_meal(meal_id, nutrition_id):
    meal = models.Meal.query.get(meal_id)
    nutrition = models.Nutrition.query.get(nutrition_id)

    meal.nutritions.remove(nutrition)
    models.db.session.commit()

app.route('/remove_nutrition_from_meal/<int:meal_id>/<int:nutrition_id>', methods=["DELETE"])(remove_nutrition_from_meal)

if __name__ == '__main__':
  port = os.environ.get('PORT') or 5000
  app.run('0.0.0.0', port=port, debug=True)