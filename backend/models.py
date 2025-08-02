# contains all our database models.
# relative import from config.py - import the instance which gives us access to sqlalchemy
from config import db

# create a class - database model represented as a Python class
class Contact(db.Model):
    # fields (name = db.Column(db.type(limit if string), unique index key = T/F, nullable (accept null) = T/F))
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(80), unique = False, nullable = False)
    last_name = db.Column(db.String(80), unique = False, nullable = False)
    email = db.Column(db.String(120 ), unique = True, nullable = False)
    
    # function - can take all of the fields above --> convert into a python dictionary --> convert into JSON --> pass from API
    # the API will send JSON back and forth for creating different objects.
    def to_json(self):
        return {
            # json requires camel case
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }