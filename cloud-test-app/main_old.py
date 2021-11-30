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
import base64
import zipfile

app = fk.Flask(__name__, template_folder="templates")
api = fkr.Api(app)


# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
MAX_RESULTS_PER_PAGE = 10
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}
ALLOWED_EXTENSIONS = {'zip'}

def allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

def round_up(dividend, divisor) -> int:
    output = int(dividend // divisor + (dividend % divisor > 0))
    return output

def parseJson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)

    return data

def getMetadataByID(ID):    #Function should return metadata as JSON from given ID as string
    #TODO metadata_JSON = sql_lookup
    metadata_JSON = {"content": "in getMetadataByID"}
    return metadata_JSON

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

def format_json_string(json_as_string)->str:
    jsonData = json.loads(json_as_string)
    data = {}
    data['repository'] = jsonData['repository']
    try:
        data['dependencies'] = list(jsonData['dependencies'].values())
    except:
        pass
        #data['dependencies'] = []
    return str(data)

def makeIdentifiers(packagejson) -> str:
    packagedict = json.loads(packagejson)
    ID = str(packagedict.get('name')) + str(packagedict.get('version'))
    version = str(packagedict.get('version'))
    name = str(packagedict.get('name'))
    return ID, name, version

def zipLogic(zip):
    #zip_IO = BytesIO(zip)
    zip_file = zipfile.ZipFile(zip)
    zip_file_jsons = []
    names_in_zip = zip_file.namelist()
    for curr_file in names_in_zip:
        if curr_file.endswith('json') and ('package.json' in curr_file):
            #print(curr_file, "\n\n\n")
            zip_file_jsons.append(zip_file.open(curr_file).read())
    zip_file.close()
    return zip_file_jsons[0].decode("utf-8")

@app.route('/')
def homepage():

    return fk.render_template('root.html')

@app.route('/reset')
def reset():

    return fk.render_template('reset_warning.html')

@app.route('/reset-confirmed', methods=["GET", "POST"])
def resetConfirmed():
    #TODO Make sure to remove SQL database items as well
    if fk.request.method == 'GET':
        return redirect('/')
    gcs = storage.Client()

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
    bytes = target_blob.download_as_bytes()
    bytes_as_file = BytesIO(bytes)

    return fk.send_file(bytes_as_file, as_attachment=True, attachment_filename=target_name)




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
        #print(type(uploaded_file))
        # blob = bucket.blob(uploaded_file.filename)

        # blob.upload_from_string(
        #     uploaded_file.read(),
        #     content_type=uploaded_file.content_type
        # )

        ############################ CHANGE LATER
        orig_data = uploaded_file.read()
        #print(len(orig_data))
        orig_contenttype = uploaded_file.content_type
        #print(orig_contenttype)
        # zip_file = zipfile.ZipFile(file_holder)
        # zip_file_jsons = []
        # names_in_zip = zip_file.namelist()
        # for curr_file in names_in_zip:
        #     if curr_file.endswith('json') and ('package.json' in curr_file):
        #         #print(curr_file, "\n\n\n")
        #         zip_file_jsons.append(zip_file.open(curr_file).read())
        # zip_file.close()
        json_as_string = zipLogic(uploaded_file)
        fileID, fileName, fileVersion = makeIdentifiers(json_as_string)
        fileID = fileID + ".zip"
        #print("Uploaded filename before: ", uploaded_file.filename)
        uploaded_file.filename = secure_filename(fileID)
        #print("Uploaded filename after: ", uploaded_file.filename)
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

        # blob.upload_from_string(
        #     uploaded_file.read(),
        #     content_type=uploaded_file.content_type
        # )
        blob.upload_from_string(
            orig_data,
            content_type=orig_contenttype
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



class APIHome(fkr.Resource):
    def get(self):

        printout={
            "description": "Welcome to the Package Manager API!", 
            "Available Commands": {
                "View Packages" : "/packages",
                "Reset System" : "/reset",
                "Upload Package" : "/package",
                "Package by Name" : "/package/byName/{name}",
                "Package by ID" : "/package/{id}",
                "Package Rating by ID" : "/package/{id}/rate"
            }
        } 
        return printout
        
    def options(self):
        return 'Error in Options for APIHome', 400

api.add_resource(APIHome, '/api')

class UploadPackage(fkr.Resource):
    def post(self):
        #print("In POST")
        #Read payload as json
        input_json = fkr.request.get_json()
        #Get file content as 64-bit encoded String
        file_string = input_json['data']['Content']
        file_ID_raw = str(input_json['metadata']['ID'])
        file_ID = secure_filename(file_ID_raw + ".zip")#Set filename for storage on GCP (Storage and SQL)

        decoded_data = base64.b64decode(bytes(file_string, 'utf-8'))    #Make into bytes

        #Make zipfile object and grab 'package.json' TODO Add this to requirements
        uploaded_file = BytesIO(decoded_data)
        zip_file = zipfile.ZipFile(uploaded_file, "r")
        zip_file_jsons = []
        names_in_zip = zip_file.namelist()
        for curr_file in names_in_zip:
            if curr_file.endswith('json') and ('package.json' in curr_file):
                zip_file_jsons.append(zip_file.open(curr_file).read())

        json_as_string = zip_file_jsons[0].decode("utf-8")
        print(json_as_string)

        gcs = storage.Client()
        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
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

        blob.upload_from_string(uploaded_file.read(),content_type=uploaded_file.content_type)

        return {'data': json_as_string}

    def options(self):
        return 'Error in Options for UploadPackage', 400

api.add_resource(UploadPackage, '/api/package')



class ViewPackages(fkr.Resource):
    def post(self, offset=1):

        curr_page = offset

        try:
            curr_page = int(curr_page)
        except:
            curr_page = 1

        gcs = storage.Client()


        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

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

        for  index_blobs, blob in enumerate(bucket.list_blobs(max_results=max_results)):
            if index_blobs >= ((curr_page-1) * MAX_RESULTS_PER_PAGE):
                #print("Blob index is: ",index_blobs, " with name ", blob.name, " on page ", page)
                
                blob_tuple = (index_blobs, blob.name)
                package_identifiers.append(blob_tuple)
                #TODO Look up package metadata in SQL from package_identifier. This metadata is what will be returned in JSON format.

        return {'description': 'in get ViewPackages'}

    def options(self):
        return 'Error in Options for UploadPackage', 400

api.add_resource(ViewPackages, '/api/packages')



class DeletePackages(fkr.Resource):
    def delete(self):
        try:
            #TODO Make sure to remove SQL database items as well
            gcs = storage.Client()

            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
            blobs = [blob_new.name for blob_new in bucket.list_blobs()] # List all the blobs available
            for target_name in blobs:
                target_blob = bucket.blob(target_name)  #Get the right blob by filename
                target_blob.delete()



            return {"description": "Registry is reset"}, 200
        except:
            return {"description": "Error in return"}, 400

    def options(self):
        return 'Error in Options for UploadPackage', 400

api.add_resource(DeletePackages, '/api/reset')



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)