# MODELS.PY
import os
from flask import Flask

from flask import render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AddOwner, AddForm, DelForm

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'my secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Puppy(db.Model):

    __tablename__ = 'puppies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    toys = db.relationship('Toy',backref='puppy',lazy='dynamic')

    owner = db.relationship('Owner',backref='puppy',uselist=False)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"Puppy name if {self.name} and owner is {self.owner.name}"
        else:
            return f"Puppy's name: {self.name} and no owner assigned yet!"

    def report_toys(self):
        print('Here are my toys:')
        for toy in self.toys:
            print(toy.item_name)

class Toy(db.Model):

    __tablename__ = 'toys'

    id = db.Column(db.Integer,primary_key=True)
    item_name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self,item_name,puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id

class Owner(db.Model):

    __tablename__ = 'Owners'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def  __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id

    def __repr__(self):
        return self.name
########################## V-Function -- HAVE FORMS

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET','POST'])
def add_pup():

    form = AddForm()

    if form.validate_on_submit():

        name = form.name.data

        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('add.html',form=form)

@app.route('/list')
def list_pup():

    puppies = Puppy.query.all()
    return render_template('list.html',puppies=puppies)

@app.route('/delete,',methods=['GET','POST'])
def del_pup():

    form = DelForm()

    if form.validate_on_submit():

        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('delete.html', form=form)

@app.route('/add_owner',methods=['GET','POST'])
def add_owner():

    form = AddOwner()

    if form.validate_on_submit():

        name = form.name.data
        id = form.pup_id.data

        new_owner = Owner(name,pup_id)
        db.session.add(new_owner)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('add_owner.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
