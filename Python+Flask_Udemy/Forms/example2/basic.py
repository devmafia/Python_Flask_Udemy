from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,BooleanField,DateTimeField,RadioField,
                    SelectField,TextField,TextAreaField,SubmitField)
from flask import flash
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):

    breed = StringField('What breed are you?', validators=[DataRequired()])
    neutered = BooleanField("Have you been neutered?")
    mood = RadioField('Please choose your mood:', choices=[('mood_one','Happy'), ('mood_two','Excited')])
    food_choice = SelectField(u'Pick your favorite food:',choices=[('chi','Chicken'),('bf','Beef'),('fish','Fish')])

    feedback = TextAreaField()
    submit = SubmitField('Submit')

class SimpleForm(FlaskForm):
    breed = StringField('What breed are you?', validators=[DataRequired()])
    submit = SubmitField('Click Me.')

@app.route('/', methods=['GET','POST'])
def index():

    form = InfoForm()
    if form.validate_on_submit():
        session['breed'] = form.breed.data
        session['neutered'] = form.neutered.data
        session['mood'] = form.mood.data
        session['food'] = form.food_choice.data
        session['feedback'] = form.feedback.data

        return redirect(url_for('thankyou'))

    return render_template('index.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/flash', methods=['GET','POST'])
def app_flash():

    form = SimpleForm()
    if form.validate_on_submit():
        session['breed'] = form.breed.data
        flash("Thank you for chooseing your breed!")
        flash('You just clicked the button!')

        return redirect(url_for('index'))
    return render_template('flash.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
