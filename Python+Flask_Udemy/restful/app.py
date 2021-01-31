import os
from flask import Flask, request
from flask_restful import Resource, Api
from secure_check import authenticate,identity
from flask_jwt import JWT ,jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

jwt = JWT(app, authenticate, identity)

# Later on this will be a model call to our database!
# Right now its just a list of dictionaries
# puppies = [{'name':'Rufus'},{name:'Frankie'},......]
# Keep in mind, its in memory, it clears with every restart!
puppies = []
class Puppy(db.Model):
    name = db.Column(db.String(80),primary_key=True)

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'name': self.name }


class PuppyNames(Resource):

    def get(self,name):

        pup = Puppy.query.filter_by(name=name),first()

        if pup:
            return pup.json()

        # Cycle through list for puppies
        for pup in puppies:
            if pup['name'] == name:
                return pup

        # If you request a puppy not yet in the puppies list
        return {'name':None},404

    def post(self, name):
        # Add  the dictionary to list
        pup = {'name':name}
        db.session.add(pup)
        db.session.commit()
        puppies.append(pup)
        # Then return it back

        return pup.json()

    def delete(self,name):

        pup = Puppy.query.filter_by(name=name).first()
        db.session.delete(pup)
        db.session.commit()

        return {'note':'delete successful'}

        # Cycle through list for puppies
        for ind,pup in enumerate(puppies):
            if pup['name'] == name:
                # don't really need to save this
                delted_pup = puppies.pop(ind)
                return {'note':'delete successful'}




class AllNames(Resource):

    #@jwt_required()
    def get(self):
        puppies = Puppy.query.all()
        # return all the puppies :)
        #return {'puppies': puppies}
        return [pup.json() for pup in puppies]


api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames,'/puppies')

if __name__ == '__main__':
    app.run(debug=True)
