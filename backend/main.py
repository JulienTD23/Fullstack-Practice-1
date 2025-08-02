# contains the main roots/endpoints
# required routes: CRUD app, so create, read/get, update, delete 
# jsonify - return json data
from flask import request, jsonify
from config import app, db
from models import Contact

# Create requires: first_name, last_name, email
# Request type: POST
@app.route("/create_contact", methods=["POST"])
def create_contact():
    # get the data associated with the contact we want to create
    # look at the submitted JSON data, make sure it's valid
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    
    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name, or email address!"}),
            400, # response error code for bad request
        )
    # if valid:
    # make a new contact object
    new_contact = Contact(first_name = first_name, last_name = last_name, email = email)
    # add it to the database w/ error checking
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    # let them know it was successful
    return jsonify({"messsage": "User created!"}), 201 #specific error code

# Get requires:
# Request type: GET
# Decorator (comes before a function) - specify the route of the endpoint we go to, and what valid methods for this URL.
@app.route("/contacts", methods=["GET"])
def get_contacts():
    # uses flask sqlalchemy to get a list of all the different contacts that exist into the database.
    contacts = Contact.query.all()
    # convert python objects into JSON 
    # lambda function - contacts is a list of contact objects with a to_json method; map the to_json onto each object
    json_contacts = list(map(lambda x: x.to_json(), contacts)) 
    return (
        jsonify({"contacts": json_contacts}),
        200, # response error code for valid request. not necessary, default
    )

# Update requires: what contact it is, what data we are updating, what data to perform the update with
# Request type: PATCH
@app.route("/update_contact/<int:user_id>", methods=["PATCH"]) #path parameter, indicating the exact contact to update
def update_contact(user_id):
    # find the user with this ID, store their object
    contact = Contact.query.get(user_id)
    # check if they exist
    if not contact:
        return jsonify({"message": "User not found"}), 404 # error code for not found
    # if exists, parse thru JSON data
    data = request.json
    # modify contact object's data for first_name to be equal to whatever the jsondata first_name is that was given to us.
    # .get looks for a key inside of a dictionary (request.json) and if exists, returns that value.
    # if firstName doesn't exist, it defaults to contact.first_name, which just means it stays the same.
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    # object was added in the session in line 1, so now we commit the change permanently
    db.session.commit()
    
    return jsonify({"message": "User updated their contact info!"}), 201

# Delete requires: what contact it is, what contact we are deleting
# Request type: DELETE
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    # same from Update
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({"message": "User not found"}), 404 # error code for not found
    
    db.session.delete(contact)
    db.session.commit()
    
    return jsonify({"message": "User deleted their contact."}), 200

# run flask application - checks if file is ran correctly. Protects from running if imported.
if __name__ == "__main__":
    # instanciate our database - when we start the app, get the context of app, then create all of the models we defined in the database (if not created)
    # Do we have the database? if not, let's do it.
    with app.app_context():
        db.create_all()
        
    app.run(debug = True)