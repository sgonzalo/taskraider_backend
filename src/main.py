"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Company, CompanyProfile, UserProfile, Login, Signup #JobPosting
#from actions import add_user
#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

##### Handle/serialize errors like a JSON object #####

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

##### generate sitemap with all your endpoints #####

@app.route('/')
def sitemap():
    return generate_sitemap(app)

 ################################################################
 ################################################################
 #SIGNUP
 ################################################################
 ################################################################

@app.route('/signup', methods=['POST', 'GET'])
def get_Signup():

##### Sign Up #####

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            body['password'] = None
        signup1 = Signup(email = body['email'], password = body['password'])
        db.session.add(signup1)
        db.session.commit()
        return "ok", 200

    ###### GET REQUEST METHOD ######

    if request.method == 'GET':
        all_signup = Signup.query.all()
        all_signup = list(map(lambda x: x.serialize(), all_signup))
        return jsonify(all_signup), 200
    return "Invalid Method", 404


@app.route('/signup/<int:signup_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_signup(signup_id):

    ###### REQUEST METHOD PUT ######

    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        signup1 = Signup.query.get(signup_id)
       
        if signup1 is None:
            raise APIException("User not found", status_code=404)
    
        if "email" in body:
            signup1.email= body["email"]
        if "password" in body:
            signup1.password= body["password"]
        db.session.commit()

        return jsonify(signup1.serialize()), 200

    ###### GET REQUEST METHOD ######

    if request.method == 'GET':
        signup1 = Signup.query.get(signup_id)
        if signup1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(signup1.serialize()), 200
    
    ###### DELETE METHOD ######

    if request.method == "DELETE":
        signup1 = Signup.query.get(signup_id)
        if signup1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(signup1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404 

 ################################################################
 ################################################################
 #LOGIN
 ################################################################
 ################################################################ 

@app.route('/login', methods=['POST', 'GET'])
def get_Login():

##### USER LOGIN #####

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            body['password'] = None
        login1 = Login(email = body['email'], password = body['password'])
        db.session.add(login1)
        db.session.commit()
        return "ok", 200

    ###### GET REQUEST METHOD ######

    if request.method == 'GET':
        all_login = Login.query.all()
        all_login = list(map(lambda x: x.serialize(), all_login))
        return jsonify(all_login), 200
    return "Invalid Method", 404

    ###### REQUEST METHOD PUT ######

    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        login1 = Login.query.get(login_id)
       
        if login1 is None:
            raise APIException("User not found", status_code=404)
    
        if "email" in body:
            login1.email= body["email"]
        if "password" in body:
            login1.password= body["password"]
        db.session.commit()

        return jsonify(login1.serialize()), 200

    ###### GET REQUEST METHOD ######

    if request.method == 'GET':
        login1 = Login.query.get(login_id)
        if login1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(login1.serialize()), 200
    
    ###### DELETE METHOD ######

    if request.method == "DELETE":
        login1 = Login.query.get(login_id)
        if login1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(login1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404 


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
            body['password'] = None
        if "re_password" not in body:
            raise APIException('You need to specify the correct password', status_code=400)
        if "username" not in body:
            raise APIException('You need to specify the username', status_code=400)
        if "skills" not in body:
            raise APIException('You need to specify the skills', status_code=400)
        
        # add_user(body)
        return "ok", 200
    
    ###### GET REQUEST METHOD ######

    if request.method == 'GET':
        all_user = User.query.all()
        all_user = list(map(lambda x: x.serialize(), all_user))
        return jsonify(all_user), 200
    return "Invalid Method", 404

@app.route('/user/<int:user_id>', methods= ['PUT', 'GET', 'DELETE'])
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
        if "re_password" in body:
            user1.re_password= body["re_password"]
        if "username" in body:
            user1.username= body["username"]
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

@app.route('/userprofile', methods=['POST', 'GET'])
def get_UserProfile():

##### Create a UserProfile and retrieve all UserProfiles ######

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "skills" not in body:
            raise APIException('You need to specify the full_name', status_code=400)
        if 'contact_info' not in body:
            raise APIException('You need to specify the email', status_code=400)
        userprofile1 = UserProfile(skills=body['skills'], contact_info = body['contact_info'])
        db.session.add(userprofile1)
        db.session.commit()
        return "ok", 200
    
    ##### GET REQUEST METHOD #####

    if request.method == 'GET':
        all_userprofile = UserProfile.query.all()
        all_userprofile = list(map(lambda x: x.serialize(), all_userprofile))
        return jsonify(all_userprofile), 200
    return "Invalid Method", 404

@app.route('/userprofile/<int:userprofile_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_userprofile(userprofile_id):

    ##### REQUEST METHOD PUT #####

    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        userprofile1 = UserProfile.query.get(userprofile_id)
       
        if userprofile1 is None:
            raise APIException("User not found", status_code=404)
        
        if "skills" in body:
            userprofile1.skills= body["skills"]
        if "contact_info" in body:
            userprofile1.contact_info= body["contact_info"]
        db.session.commit()

        return jsonify(userprofile1.serialize()), 200

    ##### GET REQUEST METHOD ######

    if request.method == 'GET':
        userprofile1 = User.query.get(user_id)
        if userprofile1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(userprofile1.serialize()), 200
    
    ##### DELETE METHHOD #####

    if request.method == "DELETE":
        userprofile1 = Userprofile.query.get(userprofile_id)
        if userprofile1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(userprofile1)
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
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            body['password'] = None
        if "re_password" not in body:
            raise APIException('You need to specify the correct password', status_code=400)
        if "address" not in body:
            raise APIException('You need to specify the address', status_code=400)
        if "company_description" not in body:
            raise APIException('You need to specify the description', status_code=400)
        company1 = Company(email = body['email'], password = body['password'], re_password=body['re_password'], address=body['address'], company_description=body['company_description'], )
        db.session.add(company1)
        db.session.commit()
        return "ok", 200
    
    #### GET REQUEST METHOD #####

    if request.method == 'GET':
        all_company = Company.query.all()
        all_company = list(map(lambda x: x.serialize(), all_company))
        return jsonify(all_company), 200
    
    return "Invalid Method", 404


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
        if "re_password" in body:
            company1.re_password= body["re_password"]
        if "username" in body:
            company1.username= body["username"]
        if "skills" in body:
            company1.skills= body["skills"]
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

@app.route('/companyprofile', methods=['POST', 'GET'])
def get_CompanyProfile():

##### Create an Company Profile and retrieve all Company Profiles #####

    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "company_info" not in body:
            raise APIException('You need to specify the full_name', status_code=400)
        companyprofile1 = CompanyProfile(company_info=body['company_info'])
        #employerprofile1.profile = EmployerProfile(company_info=body['company_info'])
        db.session.add(companyprofile1)
        db.session.commit()
        return "ok", 200
    
    ##### GET REQUEST METHOD ######

    if request.method == 'GET':
        all_companyprofile = CompanyProfile.query.all()
        all_companyprofile = list(map(lambda x: x.serialize(), all_companyprofile))
        return jsonify(all_companyprofile), 200
    return "Invalid Method", 404

@app.route('/companyprofile/<int:companyprofile_id>', methods= ['PUT', 'GET', 'DELETE'])
def get_single_companyprofile(companyprofile_id):

    ##### REQUEST METHOD PUT ######

    if request.method == "PUT":
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        companyprofile1 = CompanyProfile.query.get(companyprofile_id)
       
        if companyprofile1 is None:
            raise APIException("User not found", status_code=404)
        
        if "company_info" in body:
            companyprofile1.company_info= body["company_info"]
        db.session.commit()

        return jsonify(companyprofile1.serialize()), 200

    ##### GET REQUEST METHOD #####

    if request.method == 'GET':
        companyprofile1 = CompanyProfile.query.get(company_id)
        if companyprofile1 is None:
            raise APIException("User not found", status_code=404)
        return jsonify(companyprofile1.serialize()), 200
    
    ##### DELETE METHOD #####

    if request.method == "DELETE":
        companyprofile1 = CompanyProfile.query.get(companyprofile_id)
        if companyprofile1 is None:
            raise APIException("User not found", status_code=404)
        db.session.delete(companyprofile1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


     
# this only runs if `$ python src/main.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

##################################################################
##################################################################
 #Job Posting (Company)
##################################################################
##################################################################

# @app.route('/jobposting', methods=['POST', 'GET'])
# def jobposting():

# ##### Create a Job Posting and retrieve all job posts #####

#     if request.method == 'POST':
#         body = request.get_json()
#         if body is None:
#             raise APIException("You need to specify the request body as a json object", status_code=400)
#         if "job_title" not in body:
#             raise APIException('You need to specify the job_title', status_code=400)
#         if 'job_description' not in body:
#             raise APIException('You need to specify the job_description', status_code=400)
#         if 'zip_code' not in body:
#             raise APIException('You need to specify the zip_code', status_code=400)
#         if 'job_date' not in body:
#             raise APIException('You need to specify the job_date', status_code=400)
#         if 'skills_needed' not in body:
#             raise APIException('You need to specify the skills_needed', status_code=400)
#         if 'hours_expected' not in body:
#             raise APIException('You need to specify the hours_expected', status_code=400)
#         if 'payment' not in body:
#             raise APIException('You need to specify the payment', status_code=400)
#         jobposting1 = JobPosting(job_title=body['job_title'], job_description = body['job_description'], zip_code = body['zip_code'], job_date = body['job_date'], skills_needed = body['skills_needed'], hours_expected = body['hours_expected'], payment = body['payment'])
#         db.session.add(employer1)
#         db.session.commit()
#         return "ok", 200
    
#     ##### GET REQUEST METHOD #####

#     if request.method == 'GET':
#         all_jobposting = JobPosting.query.all()
#         all_jobposting = list(map(lambda x: x.serialize(), all_jobposting))
#         return jsonify(all_jobposting), 200
    
#     return "Invalid Method", 404


# @app.route('/jobposting/<int:jobposting_id>', methods= ['PUT', 'GET', 'DELETE'])
# def get_single_job_posting(jobposting_id):

#     ##### #REQUEST METHOD PUT ######

#     if request.method == "PUT":
#         body = request.get_json()

#         if body is None:
#             raise APIException("You need to specify the request body as a json object", status_code=400)
#         jobposting1 = JobPosting.query.get(jobposting_id)
       
#         if jobposting1 is None:
#             raise APIException("User not found", status_code=404)
        
#         if "job_title" in body:
#             jobposting1.job_title= body["job_title"]
#         if "job_description" in body:
#             jobposting1.job_description= body["job_description"]
#         if "zip_code" in body:
#             jobposting1.zip_code= body["zip_code"]
#         if "job_date" in body:
#             jobposting1.job_date= body["job_date"]
#         if "skills_needed" in body:
#             jobposting1.skills_needed= body["skills_needed"]
#         if "hours_expected" in body:
#             jobposting1.hours_expected= body["hours_expected"]
#         if "payment" in body:
#             jobposting1.payment= body["payment"]
        
#         db.session.commit()

#         return jsonify(jobposting1.serialize()), 200

#     ###### GET REQUEST METHOD ######

#     if request.method == 'GET':
#         jobposting1 = JobPosting.query.get(jobposting_id)
#         if jobposting1 is None:
#             raise APIException("User not found", status_code=404)
#         return jsonify(jobposting1.serialize()), 200
    
#     ###### DELETE REQUEST METHOD ######

#     if request.method == "DELETE":
#         jobposting1 = JobPosting.query.get(jobposting_id)
#         if jobposting1 is None:
#             raise APIException("User not found", status_code=404)
#         db.session.delete(jobposting1)
#         db.session.commit()
#         return "ok", 200

#     return "Invalid Method", 404