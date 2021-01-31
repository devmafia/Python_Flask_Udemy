from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/signup_form', methods=['GET'])
def signup_form():
    return render_template('signup_form.html')

@app.route('/report', methods=['GET'])
def report():
    upper = False
    lower = False
    num_end = False

    username = request.args.get("name")
    upper = any(w.isupper() for w in username)
    lower = any(w.islower() for w in username)
    num_end = username[-1].isdigit()
    
    return render_template('report.html', upper=upper, lower=lower, num_end=num_end)

if __name__ == '__main__':
    app.run(debug=True)
