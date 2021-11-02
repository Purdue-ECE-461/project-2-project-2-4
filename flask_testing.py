from flask import render_template
import connexion

# Create the application instance
options = {"swagger_ui": False}
app = connexion.App(__name__, specification_dir='./', options=options)

# Read the swagger.yml file to configure the endpoints
app.add_api('ECE_461_Fall_2021_Project_2_spec_v1.0.yaml')

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)