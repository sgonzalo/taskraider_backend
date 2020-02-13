"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, send_mail
from models import db, User, Company, JobPosting 
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
#####JWT####
app.config['JWT_SECRET_KEY'] = 'secret_key' 
jwt = JWTManager(app)
#######################


##### Handle/serialize errors like a JSON object #####

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

##### generate sitemap with all your endpoints #####

@app.route('/')
def sitemap():
    return generate_sitemap(app)

 
 ################################################
# JWT
################################################
# Setup the Flask-JWT-Simple extension for example


# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email in request"}), 400
    if not password:
        return jsonify({"msg": "Missing password in request"}), 400

    # check for user in database
    usercheck = User.query.filter_by(email=email, password=password).first()
    companycheck = Company.query.filter_by(email=email, password=password).first()
    # if user not found
    if usercheck is None and companycheck is None:
        return jsonify({"msg": "Invalid credentials provided"}), 401

    #if user found, Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=email), user: usercheck, company: companycheck}
    return jsonify(ret), 200

 ################################################################
 ################################################################
 #USER
 ################################################################
 ################################################################   

@app.route('/user', methods=['POST', 'GET'])

def get_User():

##### Create a USER and retrieve all Users #####

    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)
        if "contact_info" not in body:
            raise APIException('You need to specify the contact_info', status_code=400)
        if "name" not in body:
            raise APIException('You need to specify the name', status_code=400)
        if "skills" not in body:
            raise APIException('You need to specify the skills', status_code=400)
        user1 = User(email = body['email'], password = body['password'], contact_info=body['contact_info'], name=body['name'],skills=body['skills'], )
        db.session.add(user1)
        db.session.commit()
        return "ok", 200
    
    ###### GET REQUEST METHOD ######

    if request.method == 'GET':
        user1 = User.query.all()
        user1 = list(map(lambda x: x.serialize(), user1))
        return jsonify(user1), 200
   
    return "Invalid Method", 404

@app.route('/user/<int:user_id>', methods= ['PUT', 'GET', 'DELETE'])
# @jwt_required
def get_single_user(user_id):

    ###### REQUEST METHOD PUT ######

    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        user1 = User.query.get(user_id)
       
        if user1 is None:
            raise APIException("User not found", status_code=404)
        if "email" in body:
            user1.email= body["email"]
        if "password" in body:
            user1.password= body["password"]
        if "contact_info" in body:
            user1.contact_info= body["contact_info"]
        if "name" in body:
            user1.name= body["name"]
        if "skills" in body:
            user1.skills= body["skills"]

        db.session.commit()

        return jsonify(user1.serialize()), 200

    ###### GET REQUEST METHOD ######

    if request.method == 'GET':
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(user1.serialize()), 200
    
    ###### DELETE METHOD ######

    if request.method == "DELETE":
        user1 = User.query.get(user_id)
        if user1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(user1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


 ############################################################
 ############################################################
 #COMPANY
 ############################################################
 ############################################################ 

@app.route('/company', methods=['POST', 'GET'])
def get_Company():

##### Create a Company and retrieve all Companies ######

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body or body['email'] == '':
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            body['password'] = None
        if "address" not in body:
            raise APIException('You need to specify the address', status_code=400)
        if "company_name" not in body:
            raise APIException('You need to specify the company_name', status_code=400)
        if "company_description" not in body:
            raise APIException('You need to specify the description', status_code=400)

        _company = Company.query.filter_by(email=body['email']).first()
        if(_company is not None):
            raise APIException("Company already registered")

        company1 = Company(email = body['email'], password = body['password'], address=body['address'], company_name=body['company_name'],company_description=body['company_description'], )
        db.session.add(company1)
        db.session.commit()
        return jsonify(company1.serialize()), 200
    
    #### GET REQUEST METHOD #####

    if request.method == 'GET':
        all_company = Company.query.all()
        all_company = list(map(lambda x: x.serialize(), all_company))
        return jsonify(all_company), 200
    
    return "Invalid Method", 404

@app.route('/test_email', methods=['GET'])
def test_send_email():
    send_mail(["santiago.gonzalo360@gmail.com"], "A user has submitted a question", 
    "Hello fellow Task Raider! Your application has been received! You will be contacted shortly!" " "
     
    )
    return "Succesfully sent", 200

@app.route('/test_email_two', methods=['GET'])
def test_send_email2():
    send_mail(["santiago.gonzalo360@gmail.com"], "A user has applied to your post!", 
    "Test company email!" " "
    
     
    )
    return "Succesfully sent", 200
# @app.route('/test_email_two', methods=['POST'])
# def test_send_email2():
#     body = request.get_json()


#     send_mail(["santiago.gonzalo360@gmail.com"], "A user has submitted a question", 
#     "Hello fellow Task Raider! Your application has been received! You will be contacted shortly!" " "
#     )
#     return "Succesfully sent", 200
@app.route('/company/<int:company_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_company(company_id):

    #### #REQUEST METHOD PUT #####

    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        company1 = Company.query.get(company_id)
       
        if company1 is None:
            raise APIException("User not found", status_code=404)
        if "email" in body:
            company1.email= body["email"]
        if "password" in body:
            company1.password= body["password"]
        if "address" in body:
            company1.address= body["address"]
        if "company_name" in body:
            company1.company_name= body["company_name"]
        if "company_description" in body:
            company1.company_description= body["company_description"]
        db.session.commit()

        return jsonify(company1.serialize()), 200

    ##### GET REQUEST METHOD #####

    if request.method == 'GET':
        company1 = Company.query.get(company_id)
        if company1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(company1.serialize()), 200
    
    ##### DELETE METHHOD ######

    if request.method == "DELETE":
        company1 = Company.query.get(company_id)
        if company1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(company1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


     
# this only runs if `$ python src/main.py` is executed
#################################################################
#################################################################
 #Job Posting (Company)
#################################################################
#################################################################

@app.route('/jobposting', methods=['POST', 'GET'])
def jobposting():

##### Create a Job Posting and retrieve all job posts #####

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "job_title" not in body:
            raise APIException('You need to specify the job_title', status_code=400)
        if 'job_description' not in body:
            raise APIException('You need to specify the job_description', status_code=400)
        if 'zip_code' not in body:
            raise APIException('You need to specify the zip_code', status_code=400)
        if 'job_date' not in body:
            raise APIException('You need to specify the job_date', status_code=400)
        if 'skills_needed' not in body:
            raise APIException('You need to specify the skills_needed', status_code=400)
        if 'hours_expected' not in body:
            raise APIException('You need to specify the hours_expected', status_code=400)
        if 'payment' not in body:
            raise APIException('You need to specify the payment', status_code=400)
        if 'company_id' not in body:
            raise APIException('You need to specify the company_id', status_code=400)

        jobposting1 = JobPosting(job_title=body['job_title'], job_description = body['job_description'], zip_code = body['zip_code'], job_date = body['job_date'], skills_needed = body['skills_needed'], hours_expected = body['hours_expected'], payment = body['payment'])
        jobposting1.company_id = body['company_id']
        db.session.add(jobposting1)

        _company = Company.query.get(body['company_id'])
        db.session.merge(_company)

        # send_email(subject = "There is a new application", message="Contact on the way!", to=[_company.email] )
        
        
        db.session.commit()
        return jsonify(jobposting1.serialize()), 200
    
    ##### GET REQUEST METHOD #####

    if request.method == 'GET':
        all_jobposting = JobPosting.query.all()
        all_jobposting = list(map(lambda x: x.serialize(), all_jobposting))
        return jsonify(all_jobposting), 200
    
    return "Invalid Method", 404


@app.route('/jobposting/<int:jobposting_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_job_posting(jobposting_id):

    ##### #REQUEST METHOD PUT ######

    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        jobposting1 = JobPosting.query.get(jobposting_id)
       
        if jobposting1 is None:
            raise APIException("User not found", status_code=404)
        
        if "job_title" in body:
            jobposting1.job_title= body["job_title"]
        if "job_description" in body:
            jobposting1.job_description= body["job_description"]
        if "zip_code" in body:
            jobposting1.zip_code= body["zip_code"]
        if "job_date" in body:
            jobposting1.job_date= body["job_date"]
        if "skills_needed" in body:
            jobposting1.skills_needed= body["skills_needed"]
        if "hours_expected" in body:
            jobposting1.hours_expected= body["hours_expected"]
        if "payment" in body:
            jobposting1.payment= body["payment"]
        
        db.session.commit()

        # send_email(subject = "New App", message="Your application has been received!", to=[_company.email] )

        return jsonify(jobposting1.serialize()), 200

    ###### GET REQUEST METHOD ######

    if request.method == 'GET':
        jobposting1 = JobPosting.query.get(jobposting_id)
        if jobposting1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(jobposting1.serialize()), 200
    
    ###### DELETE REQUEST METHOD ######

    if request.method == "DELETE":
        jobposting1 = JobPosting.query.get(jobposting_id)
        if jobposting1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(jobposting1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
