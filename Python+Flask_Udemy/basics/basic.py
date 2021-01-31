from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    my_var = [1,2,3,4,5]
    return render_template("basic.html", my_var=my_var)

@app.route('/puppy_latin/<name>')
def puppy(name):
    def f_str(name):
        if name[-1] != "y":
            name = name+"y"
        elif name[-1] == "y":
            name = name[:-1] + "iful"
        return name
    return "Hi "+name+"!Your puppylatin name is {}".format(f_str(name))

if __name__ == "__main__":
    app.run(debug=True)
