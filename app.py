from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

workouts_table = db.Table('workouts_table',
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id')),
    db.Column('arms_id', db.Integer, db.ForeignKey('arms.arms_id')),
    db.Column('legs_id', db.Integer, db.ForeignKey('legs.legs_id')),
    db.Column('chest_id', db.Integer, db.ForeignKey('chest.chest_id')),
    db.Column('back_id', db.Integer, db.ForeignKey('back.back_id')),    
)

# class All_Workouts(db.Model):
#     __tablename__ = 'all_workouts'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     workout = db.relationship('Workout', backref='workout', cascade='all, delete, delete-orphan')

#     def __init__(self, user_id):
#         self.user_id = user_id


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    workout = db.relationship('Workout', backref='workout', cascade='all, delete, delete-orphan')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    arm_workout = db.relationship('ArmWorkout', backref='workout', cascade='all, delete, delete-orphan')
    leg_workout = db.relationship('LegWorkout', backref='workout', cascade='all, delete, delete-orphan')
    chest_workout = db.relationship('ChestWorkout', backref='workout', cascade='all, delete, delete-orphan')
    back_workout = db.relationship('BackWorkout', backref='workout', cascade='all, delete, delete-orphan')

    def __init__(self, user_id):
        self.user_id = user_id

class ArmWorkout(db.Model):
    __tablename__ = 'arms'

    arms_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False)
    weight = db.Column(db.Integer, unique=False)
    reps = db.Column(db.Integer, unique=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)

    def __init__(self, title, weight, reps, workout_id):
        self.title = title
        self.weight = weight
        self.reps = reps
        self.workout_id = workout_id

class LegWorkout(db.Model):
    __tablename__ = 'legs'

    legs_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False)
    weight = db.Column(db.Integer, unique=False)
    reps = db.Column(db.Integer, unique=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)

    def __init__(self, title, weight, reps, workout_id):
        self.title = title
        self.weight = weight
        self.reps = reps
        self.workout_id = workout_id

class ChestWorkout(db.Model):
    __tablename__ = 'chest'

    chest_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False)
    weight = db.Column(db.Integer, unique=False)
    reps = db.Column(db.Integer, unique=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)

    def __init__(self, title, weight, reps, workout_id):
        self.title = title
        self.weight = weight
        self.reps = reps
        self.workout_id = workout_id

class BackWorkout(db.Model):
    __tablename__ = 'back'

    back_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False)
    weight = db.Column(db.Integer, unique=False)
    reps = db.Column(db.Integer, unique=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)

    def __init__(self, title, weight, reps, workout_id):
        self.title = title
        self.weight = weight
        self.reps = reps
        self.workout_id = workout_id

class ArmWorkoutSchema(ma.Schema):
    class Meta:
        fields = ('arms_id','title', 'weight', 'reps', 'workout_id')

arm_workout_schema = ArmWorkoutSchema()
multiple_arm_workout_schema = ArmWorkoutSchema(many=True)

class LegWorkoutSchema(ma.Schema):
    class Meta:
        fields = ('legs_id', 'title', 'weight', 'reps', 'workout_id')

leg_workout_schema = LegWorkoutSchema()
multiple_leg_workout_schema = LegWorkoutSchema(many=True)

class ChestWorkoutSchema(ma.Schema):
    class Meta:
        fields = ('chest_id', 'title', 'weight', 'reps', 'workout_id')

chest_workout_schema = ChestWorkoutSchema()
multiple_chest_workout_schema = ChestWorkoutSchema(many=True)

class BackWorkoutSchema(ma.Schema):
    class Meta:
        fields = ('back_id', 'title', 'weight', 'reps', 'workout_id')

back_workout_schema = BackWorkoutSchema()
multiple_back_workout_schema = BackWorkoutSchema(many=True)

class WorkoutSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'arm_workout', 'leg_workout', 'chest_workout', 'back_workout')
    arms = ma.Nested(multiple_arm_workout_schema)
    legs = ma.Nested(multiple_leg_workout_schema)
    chest = ma.Nested(multiple_chest_workout_schema)
    back = ma.Nested(multiple_back_workout_schema)

workout_schema = WorkoutSchema()
multiple_workout_schema = WorkoutSchema(many=True)


# class AllWorkoutsSchema(ma.Schema):
#     class Meta:
#         fields = ('workout_id', 'user_id')

# all_workouts_schema = AllWorkoutsSchema()
# multiple_all_workouts_schema = AllWorkoutsSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'workout', 'arm_workout')
    workout = ma.Nested(multiple_workout_schema)

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route('/user/add', methods=['POST'])
def add_user(): 
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')
    possible_duplicate = db.session.query(User).filter(User.username == username).first()

    if possible_duplicate is not None:
        return jsonify('Error: the username is already in use.')

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username, encrypted_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify("Let's get SWOLE")

@app.route('/user/authenticate', methods=["POST"])
def authenticate_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')
    
    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify('User NOT verified')
    if bcrypt.check_password_hash(user.password, password) == False:
        return jsonify('Password NOT verified')

    return jsonify('User has been verified')


@app.route('/users', methods=["GET"])
def get_users():
        all_users = db.session.query(User).all()
        return jsonify(multiple_user_schema.dump(all_users))

@app.route('/user/<id>', methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/user/<id>', methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return "User is no longer swole"

# @app.route('/all_workouts/add', methods=["POST"])
# def add_all_workouts():
#     if request.content_type != 'application/json':
#         return jsonify('Error: Data must be json')

#     user_id = request.json['user_id']

#     new_all_workouts = All_Workouts(user_id)

#     db.session.add(new_all_workouts)
#     db.session.commit()


#     return "A new workout has been added"

# Workouts
@app.route('/workout/add', methods=["POST"])
def add_workout():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()

    user_id = post_data.get('user_id')

    new_workout = Workout(user_id)

    db.session.add(new_workout)
    db.session.commit()


    return jsonify('A new workout has been created')

@app.route('/workout', methods=["GET"])
def get_workouts():
    all_workouts = db.session.query(Workout).all()

    return_data = generate_return_Data(workout_schema.dump(all_workouts))
    return jsonify(multiple_workout_schema.dump(all_workouts))

@app.route('/workout/delete/<id>', methods=["DELETE"])
def delete_workout(id):
    workout = db.session.query(Workout).filter(Workout.id == id).first()
    db.session.delete(workout)
    db.session.commit()

    return jsonify('The workout has been deleted')

@app.route('/workout/update/<id>', methods={"PUT", "PATCH"})
def update_workout_by_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    weight = post_data.get('weight')
    reps = post_data.get('reps')

    workout = db.session.query(Workout).filter(Workout.id == id).first()


    if title != None:
        workout.title = title
    if weight != None:
        workout.weight = weight
    if reps != None:
        workout.reps = reps

    db.session.commit()
    return jsonify('Your workout has been updated')

# Arm Workouts
@app.route('/arm_workout/add', methods=["POST"])
def add_arm_workout():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    weight = post_data.get('weight')
    reps = post_data.get('reps')
    workout_id = post_data.get('workout_id')

    new_arm_workout = ArmWorkout(title, weight, reps, workout_id)

    db.session.add(new_arm_workout)
    db.session.commit()


    return jsonify(arm_workout_schema.dump(new_arm_workout))

@app.route('/arm_workout', methods=["GET"])
def get_arm_workouts():
    all_arm_workouts = db.session.query(ArmWorkout).all()
    return jsonify(multiple_arm_workout_schema.dump(all_arm_workouts))

@app.route('/arm_workout/delete/<id>', methods=["DELETE"])
def delete_arm_workout(id):
    arm_workout = db.session.query(ArmWorkout).filter(ArmWorkout.id == id).first()
    db.session.delete(arm_workout)
    db.session.commit()

    return jsonify('The workout has been deleted')

@app.route('/arm_workout/update/<id>', methods={"PUT", "PATCH"})
def update_arm_workout_by_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    weight = post_data.get('weight')
    reps = post_data.get('reps')

    arm_workout = db.session.query(ArmWorkout).filter(ArmWorkout.id == id).first()


    if title != None:
        arm_workout.title = title
    if weight != None:
        arm_workout.weight = weight
    if reps != None:
        arm_workout.reps = reps

    db.session.commit()
    return jsonify('Your workout has been updated')


if __name__ == "__main__":
    app.run(debug=True)