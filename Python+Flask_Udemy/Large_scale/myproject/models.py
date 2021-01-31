# MODELS.PY

from myproject import db

class Toy(db.Model):

    __tablename__ = 'toys'

    id = db.Column(db.Integer,primary_key = True)
    item_name = db.Column(db.Text)
    # Connect the toy to the puppy that owns it.
    # We use puppies.id because __tablename__='puppies'
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id'))

    def __init__(self,item_name,puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id

class Puppy(db.Model):

    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    toys = db.relationship('Toy',backref='puppy',lazy='dynamic')

    owner = db.relationship('Owner',backref='owner',uselist=False)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f'Puppy name is {self.name} and owner is {self.owner.name}'
        else:
            return f'Puppy name is {self.name} and has no owner yet!'

    def report_toys(self):
        print('Here are my toys:')
        for toy in self.toys:
            print(toy.item_name)

class Owner(db.Model):

    __tablename__ = 'Owners'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def  __init__(self, name, pup_id):
        self.name = name
        self.puppy_id = pup_id
