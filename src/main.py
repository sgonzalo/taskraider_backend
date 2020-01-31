"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Employee, Employer, EmployeeProfile, EmployerProfile
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
 #######################################
 #EMPLOYEE
 #######################################   
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

@app.route('/employeeprofile', methods=['POST', 'GET'])
def get_EmployeeProfile():
#Create a EmployeeProfile and retrieve all EmployeeProfiles!!
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "skills" not in body:
            raise APIException('You need to specify the full_name', status_code=400)
        if 'contact_info' not in body:
            raise APIException('You need to specify the email', status_code=400)
        employeeprofile1 = EmployeeProfile(skills=body['skills'], contact_info = body['contact_info'])
        db.session.add(employeeprofile1)
        db.session.commit()
        return "ok", 200
    
    # GET request
    if request.method == 'GET':
        all_employeeprofile = EmployeeProfile.query.all()
        all_employeeprofile = list(map(lambda x: x.serialize(), all_employeeprofile))
        return jsonify(all_employeeprofile), 200
    return "Invalid Method", 404

@app.route('/employeeprofile/<int:employeeprofile_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_employeeprofile(employeeprofile_id):

    #REQUEST METHOD PUT
    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        employeeprofile1 = EmployeeProfile.query.get(employeeprofile_id)
       
        if employeeprofile1 is None:
            raise APIException("User not found", status_code=404)
        
        if "skills" in body:
            employeeprofile1.skills= body["skills"]
        if "contact_info" in body:
            employeeprofile1.contact_info= body["contact_info"]
        db.session.commit()

        return jsonify(employeeprofile1.serialize()), 200

    # GET request
    if request.method == 'GET':
        employeeprofile1 = Employee.query.get(employee_id)
        if employeeprofile1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(employeeprofile1.serialize()), 200
    
    #DELETE METHHOD
    if request.method == "DELETE":
        employeeprofile1 = Employeeprofile.query.get(employeeprofile_id)
        if employeeprofile1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(employeeprofile1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

 #######################################
 #EMPLOYER
 ####################################### 

@app.route('/employer', methods=['POST', 'GET'])
def get_Employer():

#Create a Employer and retrieve all Employer!!

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
        employer1 = Employer(full_name=body['full_name'], email = body['email'], password = body['password'])
        db.session.add(employer1)
        db.session.commit()
        return "ok", 200
    
    # GET request
    if request.method == 'GET':
        all_employer = Employer.query.all()
        all_employer = list(map(lambda x: x.serialize(), all_employer))
        return jsonify(all_employer), 200
    
    return "Invalid Method", 404


@app.route('/employer/<int:employer_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_employer(employer_id):

    #REQUEST METHOD PUT
    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        employer1 = Employer.query.get(employer_id)
       
        if employer1 is None:
            raise APIException("User not found", status_code=404)
        
        if "full_name" in body:
            employer1.full_name= body["full_name"]
        if "email" in body:
            employer1.email= body["email"]
        if "password" in body:
            employer1.password= body["password"]
        db.session.commit()

        return jsonify(employer1.serialize()), 200

    # GET request
    if request.method == 'GET':
        employer1 = Employer.query.get(employer_id)
        if employer1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(employer1.serialize()), 200
    
    #DELETE METHHOD
    if request.method == "DELETE":
        employer1 = Employer.query.get(employer_id)
        if employer1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(employer1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

@app.route('/employerprofile', methods=['POST', 'GET'])
def get_EmployerProfile():
#Create an EmployerProfile and retrieve all EmployerProfiles!!
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "company_info" not in body:
            raise APIException('You need to specify the full_name', status_code=400)
        employerprofile1 = EmployerProfile(company_info=body['company_info'])
        #employerprofile1.profile = EmployerProfile(company_info=body['company_info'])
        db.session.add(employerprofile1)
        db.session.commit()
        return "ok", 200
    
    # GET request
    if request.method == 'GET':
        all_employerprofile = EmployerProfile.query.all()
        all_employerprofile = list(map(lambda x: x.serialize(), all_employerprofile))
        return jsonify(all_employerprofile), 200
    return "Invalid Method", 404

@app.route('/employerprofile/<int:employerprofile_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_employerprofile(employerprofile_id):

    #REQUEST METHOD PUT
    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        employerprofile1 = EmployerProfile.query.get(employerprofile_id)
       
        if employerprofile1 is None:
            raise APIException("User not found", status_code=404)
        
        if "company_info" in body:
            employerprofile1.company_info= body["company_info"]
        db.session.commit()

        return jsonify(employerprofile1.serialize()), 200

    # GET request
    if request.method == 'GET':
        employerprofile1 = EmployerProfile.query.get(employer_id)
        if employerprofile1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(employeeprofile1.serialize()), 200
    
    #DELETE METHHOD
    if request.method == "DELETE":
        employerprofile1 = EmployerProfile.query.get(employerprofile_id)
        if employerprofile1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(employerprofile1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


     
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
