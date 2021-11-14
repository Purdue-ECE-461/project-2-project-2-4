import datetime
import subprocess
import sys
import json
import flask as fk
import flask_restful as fkr
from flask_restful import reqparse
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
#import main_api
import base64
import zipfile

app = fk.Flask(__name__, template_folder="templates")
api = fkr.Api(app)


# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
MAX_RESULTS_PER_PAGE = 10
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            #db_address = os.environ['CLOUD_SQL_IP']
            db_address = '34.123.253.38'
            return pymysql.connect(host=db_address, db=db_name, user=db_user, password=db_password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    except:
        pass
    
    pass


@app.route('/')
def homepage():


    return fk.render_template('root.html')

@app.route('/reset')
def reset():


    return fk.render_template('reset_warning.html')

@app.route('/reset-confirmed', methods=["GET", "POST"])
def resetConfirmed():
    if fk.request.method == 'GET':
        return redirect('/')
    gcs = storage.Client()

    # Get the bucket that the file will be downloaded from.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blobs = [blob_new.name for blob_new in bucket.list_blobs()] # List all the blobs available
    for target_name in blobs:
        target_blob = bucket.blob(target_name)  #Get the right blob by filename
        target_blob.delete()
    

    return fk.render_template('reset_complete.html')

@app.route('/java-version')
def javaVersion():
    output2 = subprocess.run(["./Java_install/jdk-17.0.1/bin/java", "-jar", "Main.jar"], capture_output=True) # We want this to be a string that looks like json

    version2 = output2.stdout.decode("utf-8")
    version3 = output2.stderr.decode("utf-8")
    print(output2.stdout.decode("utf-8"))
    version1 = "java placeholder"
    version1 = sys.platform
    return fk.render_template('javaversion.html', java_version1 = version1, java_version2 = version2, java_version3 = version3)

@app.route('/hiddenpage')
def rootSQRD():


    return fk.render_template('root.html')

@app.route('/upload-package')
def uploadPackage():


    return fk.render_template('upload_package.html')


@app.route('/download-package', methods=['POST'])
def downloadPackage():
    if fk.request.method == 'POST':
        get_package_index = int(fk.request.form['package_index'])

    gcs = storage.Client()

    # Get the bucket that the file will be downloaded from.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blobs = [blob_new.name for blob_new in bucket.list_blobs()] # List all the blobs available
    target_name =  blobs[get_package_index] #Get the blob name
    target_blob = bucket.blob(target_name)  #Get the right blob by filename
    #print(target_blob)
    #print(type(target_blob))
    #file_to_download = target_blob.download_to_filename(target_name)
    #print("file_to_download TYPE: ", type(file_to_download))
    bytes = target_blob.download_as_bytes()
    #bytes.seek(0,0)
    #print("FILE TYPE: ",type(file_to_download))
    #print("BYTES TYPE: ",type(bytes))
    #print("BYTES: \n\n",bytes)
    bytes_as_file = BytesIO(bytes)
    #URL_to_download = 'https://storage.googleapis.com/ece-461-project-2-team-4.appspot.com/' + target_name
    #print(URL_to_download)

    
    #return fk.render_template('download_package_success.html', URL_to_download=URL_to_download)
    #return fk.render_template('download_package_success.html')
    return fk.send_file(bytes_as_file, as_attachment=True, attachment_filename=target_name)
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    #   dummy_times = [datetime.datetime(2000, 5, 25, 10, 0, 0),
    #                  datetime.datetime(2000, 5, 25, 10, 30, 0),
    #                  datetime.datetime(2000, 5, 25, 11, 0, 0),
    #                 ]
    '''conn = connecttoDB()
    cursor = conn.cursor()
    data = parseJson("output.json")

    try:
        for entry in data["scores"]:
            cursor.execute("INSERT INTO scores_table (url, ramp_up_score, correctness_score, bus_factor_score, responsive_maintainer_score, license_score, dependency_score) VALUES(%s, %s, %s, %s, %s, %s, %s)", (entry["url"], entry["rampup"], entry["correctness"], entry["busfactor"], entry["contributors"], entry["license"], entry["dependency"]))

        conn.commit()
        pass
    except:
        pass'''
    
    #return render_template('upload_package.html')



@app.route('/view-packages', methods=['GET', 'POST'])
def viewPackages(curr_page = 1):
    fk.render_template('loading.html')
    if fk.request.method == 'POST':
        curr_page = fk.request.form['next_page']
    print("CURR PAGE1: ", curr_page)
    try:
        curr_page = int(curr_page)
    except:
        curr_page = 1
    print("CURR PAGE2: ", curr_page)
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    #blob_iter = bucket.list_blobs(bucket)
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
    package_identifiers = []
    print("CURR PAGE3: ", curr_page)
    for  index_blobs, blob in enumerate(bucket.list_blobs(max_results=max_results)):
        if index_blobs >= ((curr_page-1) * MAX_RESULTS_PER_PAGE):
            print("Blob index is: ",index_blobs, " with name ", blob.name, " on page ", page)
            blob_tuple = (index_blobs, blob.name)
            package_identifiers.append(blob_tuple)


    return fk.render_template('view_packages.html', package_identifiers=package_identifiers, curr_page=curr_page, max_pages=max_pages)




def format_json_string(json_as_string)->str:
    jsonData = json.loads(json_as_string)
    data = {}
    data['repository'] = jsonData['repository']
    data['dependencies'] = list(jsonData['dependencies'].values())
    return str(data)






@app.route('/upload', methods=['POST'])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    if fk.request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in fk.request.files:
            
            return fk.redirect(fk.request.url)
        uploaded_files = fk.request.files.getlist('files')


    
    
    
    for uploaded_file in uploaded_files:
        
        if not (uploaded_file):
            return 'No file uploaded.', 400
        if not (allowed_file(uploaded_file.filename)):
            return 'Unallowed file type uploaded. Only .zip files are accepted at this time.', 400            
        if uploaded_file.filename == '':
            return 'No selected file', 400 

        uploaded_file.name = secure_filename(uploaded_file.name)   #ensure the filename is OK for computers
        if uploaded_file.filename == '':
            return 'secure_filename broke and returned an empty filename', 400 
        
        ############################ CHANGE LATER
        zip_file = zipfile.ZipFile(uploaded_file)
        zip_file_jsons = []
        names_in_zip = zip_file.namelist()
        for curr_file in names_in_zip:
            if curr_file.endswith('json') and ('package.json' in curr_file):
                print(curr_file, "\n\n\n")
                zip_file_jsons.append(zip_file.open(curr_file).read())

        print(type(zip_file_jsons[0]))
        print(zip_file_jsons)
        #print(zip_file_jsons[0].decode("utf-8"))
        json_as_string = zip_file_jsons[0].decode("utf-8")
        print(json_as_string)
        print('BLANK LINES\n\n\n\n')

        print("SUBPROCESS OUTPUT:   ", subprocess.run(["./Java_install/jdk-17.0.1/bin/java", "-jar", "trustworthiness_copy-1.0-SNAPSHOT-jar-with-dependencies.jar", format_json_string(json_as_string)], capture_output=True))


        ################################
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
    return fk.render_template('upload_package_success.html')


@app.errorhandler(500)
def server_error(e: Union[Exception, int]) -> str:
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500




class UploadPackage(fkr.Resource):
    def post(self):
        print("In POST")
        some_json = fkr.request.get_json()
        #some_json = reqparse.RequestParser().parse_args()
        print(some_json)
        print("HERE")
        #print("REST ",fkr.request.get_json())
        #print("FLASK ",fk.request.get_json())
        print(type(some_json))
        file_string = some_json['data']['Content']
        print("FILE STRING: ", file_string)
        #file_object = base64.b64encode(file_string.read()).decode('utf-8')
        ##print(file_object)
        #print(type(file_object))
        return {'data': file_string}

    def options(self):
        print("In Options")
        some_json1 = fkr.request.get_json()
        some_json2 = reqparse.RequestParser().parse_args()
        #print("REST ",fkr.request.get_json(force=True))
        #print("FLASK ",fk.request.get_json(force=True))
        print(type(some_json1))
        print(some_json1)
        print(type(some_json2))
        print(some_json2)
        file_string = some_json1['data']['Content']
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