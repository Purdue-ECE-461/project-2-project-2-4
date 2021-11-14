from flask import (
    Flask,
    render_template
)

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')



@app.route('/<int:number>/')
def incrementer(number):
    return "Incremented number is INT " + str(number+1)
@app.route('/<int:number>/')
def incrementer2(number):
    return "Incremented number is FLOAT " + str(number+1)

@app.route('/<string:name>/')
def hello(name):
    return "Hello " + name

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)