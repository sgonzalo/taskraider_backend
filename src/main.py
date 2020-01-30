"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Employee
#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
@app.route('/employee', methods=['POST', 'GET'])
def get_Employee():
#Create a Employee and retrieve all Employees!!
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "full_name" not in body:
            raise APIException('You need to specify the full_name', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            body['password'] = None
        employee1 = Employee(full_name=body['full_name'], email = body['email'], password = body['password'])
        db.session.add(employee1)
        db.session.commit()
        return "ok", 200
    
    # GET request
    if request.method == 'GET':
        all_employee = Employee.query.all()
        all_employee = list(map(lambda x: x.serialize(), all_employee))
        return jsonify(all_employee), 200
    return "Invalid Method", 404

@app.route('/employee/<int:employee_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_employee(employee_id):

    #REQUEST METHOD PUT
    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        employee1 = Employee.query.get(employee_id)
       
        if employee1 is None:
            raise APIException("User not found", status_code=404)
        
        if "full_name" in body:
            employee1.full_name= body["full_name"]
        if "email" in body:
            employee1.email= body["email"]
        if "password" in body:
            employee1.password= body["password"]
        db.session.commit()

        return jsonify(employee1.serialize()), 200

    # GET request
    if request.method == 'GET':
        employee1 = Employee.query.get(employee_id)
        if employee1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(employee1.serialize()), 200
    
    #DELETE METHHOD
    if request.method == "DELETE":
        employee1 = Employee.query.get(employee_id)
        if employee1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(employee1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404
        
       
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
