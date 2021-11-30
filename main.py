import datetime
import subprocess
import sys
import json
import flask as fk
import flask_restful as fkr
import logging
import os
from io import BytesIO
from typing import Union
from flask.helpers import url_for
from google.cloud import storage
from google.cloud.storage import client
from werkzeug.utils import redirect, secure_filename
import pymysql
import json

app = fk.Flask(__name__, template_folder="templates")
api = fkr.Api(app)


# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
MAX_RESULTS_PER_PAGE = 10

def round_up(dividend, divisor) -> int:
    output = int(dividend // divisor + (dividend % divisor > 0))
    return output

def parseJson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)

    return data

def connecttoDB():
    db_user = os.environ['CLOUD_SQL_USERNAME']
    db_password = os.environ['CLOUD_SQL_PASSWORD']
    db_name = os.environ['CLOUD_SQL_DATABASE_NAME']
    db_connection_name = os.environ['CLOUD_SQL_CONNECTION_NAME']
    #db_address = os.environ['CLOUD_SQL_IP']
    unix_socket = '/cloudsql/{}'.format(db_connection_name)

    try:
        if os.environ.get('GAE_ENV') == 'standard':
            return pymysql.connect(unix_socket=unix_socket, db=db_name, user=db_user, password=db_password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        else:
            db_address = os.environ['CLOUD_SQL_IP']
            return pymysql.connect(host=db_address, db=db_name, user=db_user, password=db_password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    except:
        pass
    
    pass


@app.route('/')
def homepage():

    return render_template('root.html')

@app.route('/hiddenpage')
def rootSQRD():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    #   dummy_times = [datetime.datetime(2000, 5, 25, 10, 0, 0),
    #                  datetime.datetime(2000, 5, 25, 10, 30, 0),
    #                  datetime.datetime(2000, 5, 25, 11, 0, 0),
    #                 ]

    return render_template('root.html')

@app.route('/upload-package')
def uploadPackage():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    #   dummy_times = [datetime.datetime(2000, 5, 25, 10, 0, 0),
    #                  datetime.datetime(2000, 5, 25, 10, 30, 0),
    #                  datetime.datetime(2000, 5, 25, 11, 0, 0),
    #                 ]
    conn = connecttoDB()
    cursor = conn.cursor()
    data = parseJson("output.json")

    try:
        for entry in data["scores"]:
            cursor.execute("INSERT INTO scores_table (url, ramp_up_score, correctness_score, bus_factor_score, responsive_maintainer_score, license_score, dependency_score) VALUES(%s, %s, %s, %s, %s, %s, %s)", (entry["url"], entry["rampup"], entry["correctness"], entry["busfactor"], entry["contributors"], entry["license"], entry["dependency"]))

        conn.commit()
        pass
    except:
        pass
    
    return render_template('upload_package.html')

@app.route('/retrieve-package')
def retrievePackage():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    #   dummy_times = [datetime.datetime(2000, 5, 25, 10, 0, 0),
    #                  datetime.datetime(2000, 5, 25, 10, 30, 0),
    #                  datetime.datetime(2000, 5, 25, 11, 0, 0),
    #                 ]

    return render_template('retrieve_package.html')

@app.route('/view-packages', methods=['GET', 'POST'])
def viewPackages(curr_page = 1):
    render_template('loading.html')
    if request.method == 'POST':
        curr_page = request.form['next_page']
    print("CURR PAGE1: ", curr_page)
    try:
        curr_page = int(curr_page)
    except:
        curr_page = 1
    print("CURR PAGE2: ", curr_page)
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    blob_iter = bucket.list_blobs(bucket)
    #curr_page = 1                          #hard coded placeholder

    all_pages = bucket.list_blobs().pages
    total_blobs = 0
    for page in all_pages:
        total_blobs += page.num_items
    max_pages = round_up(total_blobs, MAX_RESULTS_PER_PAGE)
    if (curr_page < 1):           #Should we deal with an upper bound?
        curr_page = 1
    elif(curr_page > max_pages):
        curr_page = max_pages
    max_results = MAX_RESULTS_PER_PAGE * curr_page
    package_names = []
    print("CURR PAGE3: ", curr_page)
    for  index_blobs, blob in enumerate(bucket.list_blobs(max_results=max_results)):
        if index_blobs >= ((curr_page-1) * MAX_RESULTS_PER_PAGE):
            print("Blob index is: ",index_blobs, " with name ", blob.name, " on page ", page)
            package_names.append(blob.name)


    return render_template('view_packages.html', package_names = package_names, curr_page = curr_page, max_pages = max_pages)

@app.route('/upload', methods=['POST'])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    uploaded_files = request.files.getlist('files')
    
    for uploaded_file in uploaded_files:
        
        if not uploaded_file:
            return 'No file uploaded.', 400
        


        #Upload rate information SQL Database
        conn = connecttoDB()
        cursor = conn.cursor()
        data = parseJson("output.json")
        try:
            for entry in data["scores"]:
                cursor.execute("INSERT INTO scores_table (url, ramp_up_score, correctness_score, bus_factor_score, responsive_maintainer_score, license_score, dependency_score) VALUES(%s, %s, %s, %s, %s, %s, %s)", (entry["url"], entry["rampup"], entry["correctness"], entry["busfactor"], entry["contributors"], entry["license"], entry["dependency"]))

            conn.commit()
            pass
        except:
            pass


        # Create a new blob and upload the file's content.
        blob = bucket.blob(uploaded_file.filename)

        blob.upload_from_string(
            uploaded_file.read(),
            content_type=uploaded_file.content_type
        )

    # Make the blob public. This is not necessary if the
    # entire bucket is public.
    # See https://cloud.google.com/storage/docs/access-control/making-data-public.
    #blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    #return blob.public_url
    return render_template('upload_package_success.html')


@app.errorhandler(500)
def server_error(e: Union[Exception, int]) -> str:
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500




class UploadPackage(fkr.Resource):
    def post(self):
        some_json = fkr.request.get_json()
        file_string = some_json['data']['Content']
        file_object = base64.b64encode(file_string.read()).decode('utf-8')
        print(file_object)
        print(type(file_object))

api.add_resource(UploadPackage, '/api/upload')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)