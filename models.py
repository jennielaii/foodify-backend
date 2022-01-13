from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String, nullable=False, unique=False)
    last = db.Column(db.String, nullable=False, unique=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)

    def to_json(self):
        return {
            "id": self.id,
            "first": self.first,
            "last": self.last,
            "email": self.email
        }
        
class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    meal_name = db.Column(db.String)
    date = db.Column(db.DateTime)
    
    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "meal_name": self.meal_name,
            "date": self.date,
        }

class Nutrition(db.Model):
    __tablename__ = 'nutritions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    food_name = db.Column(db.String)
    protein = db.Column(db.String)
    carbohydrate = db.Column(db.String)
    fat = db.Column(db.String)
    calories = db.Column(db.String)
    
    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "protein": self.protein,
            "carbohydrate": self.carbohydrate,
            "fat": self.fat,
            "calories": self.calories
        }

class Meal_Nutrition(db.Model):
    __tablename__ = 'meals_nutritions'
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    nutrition_id = db.Column(db.Integer, db.ForeignKey('nutritions.id'))
    
    def to_json(self):
        return {
            "id": self.id,
            "nutrition_id ": self.nutrition_id,
        }