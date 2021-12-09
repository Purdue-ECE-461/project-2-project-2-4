import datetime
import subprocess
import sys
import json
import logging
import os
import json
import base64
import zipfile
from io import BytesIO
from typing import Union
from flask.helpers import url_for
from google.cloud import storage
from google.cloud.storage import client
from werkzeug.utils import redirect, secure_filename
from google.cloud import secretmanager

from flask import Flask, request, render_template, send_file
from flask_restful import Api, Resource, reqparse
import requests

app = Flask(__name__)
api = Api(app)

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
#APPLICATION_ID = os.environ['APPLICATION_ID']
MAX_RESULTS_PER_PAGE = 10
ALLOWED_EXTENSIONS = {'zip'}

def access_secret_version(secret_id, version_id="latest"):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/951373247679/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')
os.environ["GITHUB_TOKEN"] = access_secret_version("GITHUB_TOKEN")

def allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

def makeIdentifiers(packagejson) -> str:
    packagedict = json.loads(packagejson)
    ID = str(packagedict.get('name')) + str(packagedict.get('version'))
    version = str(packagedict.get('version'))
    name = str(packagedict.get('name'))
    return ID, name, version

def versionChecker(package_version, acceptable_versions) -> bool:
    if acceptable_versions == "ALL_VERSIONS":
        return True
    if package_version == acceptable_versions:
        return True
    if "*" in acceptable_versions:
        return True
    major, minor, patch = package_version.split(".")
    major_int = int(major)
    minor_int = int(minor)
    patch_int = int(patch)
    minor_and_patch = int(minor + patch)
    if "^" in acceptable_versions:
        acceptable_versions = acceptable_versions.replace("^", "")
        accept_major, accept_minor, accept_patch = acceptable_versions.split(".")
        accept_minor_int = int(accept_minor)
        accept_major_int = int(accept_major)
        accept_patch_int = int(accept_patch)
        if (major == accept_major_int):
            if minor_int > accept_minor_int:
                return True
            if minor_int < accept_minor_int:
                return False
            if patch_int >= accept_patch_int:
                return True
        return False
    if "~" in acceptable_versions:
        acceptable_versions = acceptable_versions.replace("~", "")
        accept_major, accept_minor, accept_patch = acceptable_versions.split(".")
        accept_patch_int = int(accept_patch)
        if (major == accept_major) and (minor == accept_minor) and (patch_int >= accept_patch_int):
            return True 
        return False
    if ">" in acceptable_versions:
        acceptable_versions = acceptable_versions.replace(">", "")
        accept_major, accept_minor, accept_patch = acceptable_versions.split(".")
        accept_patch_int = int(accept_patch)
        accept_major_int = int(accept_major)
        accept_minor_int = int(accept_minor)
        if (major_int > accept_major_int):
            return True 
        if (major_int < accept_major_int):
            return False
        if minor_int > accept_minor_int:
            return True 
        if minor_int < accept_minor_int:
            return False
        if patch_int > accept_patch_int:
            return True
        return False
    if ">=" in acceptable_versions:
        acceptable_versions = acceptable_versions.replace(">=", "")
        accept_major, accept_minor, accept_patch = acceptable_versions.split(".")
        accept_patch_int = int(accept_patch)
        accept_major_int = int(accept_major)
        accept_minor_int = int(accept_minor)
        if (major_int > accept_major_int):
            return True 
        if (major_int < accept_major_int):
            return False
        if minor_int > accept_minor_int:
            return True 
        if minor_int < accept_minor_int:
            return False
        if patch_int >= accept_patch_int:
            return True
        return False
    if "<" in acceptable_versions:
        acceptable_versions = acceptable_versions.replace("<", "")
        accept_major, accept_minor, accept_patch = acceptable_versions.split(".")
        accept_patch_int = int(accept_patch)
        accept_major_int = int(accept_major)
        accept_minor_int = int(accept_minor)
        if (major_int > accept_major_int):
            return False
        if (major_int < accept_major_int):
            return True
        if minor_int > accept_minor_int:
            return False 
        if minor_int < accept_minor_int:
            return True
        if patch_int < accept_patch_int:
            return True
        return False
    if "<=" in acceptable_versions:
        acceptable_versions = acceptable_versions.replace("<=", "")
        accept_major, accept_minor, accept_patch = acceptable_versions.split(".")
        accept_patch_int = int(accept_patch)
        accept_major_int = int(accept_major)
        accept_minor_int = int(accept_minor)
        if (major_int > accept_major_int):
            return False
        if (major_int < accept_major_int):
            return True
        if minor_int > accept_minor_int:
            return False 
        if minor_int < accept_minor_int:
            return True
        if patch_int <= accept_patch_int:
            return True
        return False
    if "-" in acceptable_versions:
        lhs, rhs = acceptable_versions.split("-")
        lhs_major, lhs_minor, lhs_patch = lhs.split(".")
        lhs_major = int(lhs_major)
        lhs_minor = int(lhs_minor)
        lhs_patch = int(lhs_patch)
        rhs_major, rhs_minor, rhs_patch = rhs.split(".")
        rhs_major = int(rhs_major)
        rhs_minor = int(rhs_minor)
        rhs_patch = int(rhs_patch)

        if (major_int > lhs_major) and (major_int < rhs_major):
            return True 
        if (major_int < lhs_major) or (major_int > rhs_major):
            return False
        if (major_int == lhs_major):
            if minor_int > lhs_minor:
                return True 
            if minor_int < lhs_minor:
                return False
            if patch_int >= lhs_patch:
                return True

        if (major_int == rhs_major):
            if minor_int > rhs_minor:
                return False 
            if minor_int < rhs_minor:
                return True
            if patch_int <= rhs_patch:
                return True
        return False
    
    return False

def round_up(dividend, divisor) -> int:
    """Simple function to round up an integer using logic"""
    output = int(dividend // divisor + (dividend % divisor > 0))
    return output

def zipLogic(zip):
    #zip_IO = BytesIO(zip)
    zip_file = zipfile.ZipFile(zip)
    zip_file_jsons = []
    names_in_zip = zip_file.namelist()
    for curr_file in names_in_zip:
        if curr_file.endswith('json') and ('package.json' in curr_file):
            zip_file_jsons.append(zip_file.open(curr_file).read())
    zip_file.close()
    return zip_file_jsons[0].decode("utf-8")

def format_json_string(json_as_string)->str:
    jsonData = json.loads(json_as_string)
    data = {}
    url = ""
    if type(jsonData['repository']) is dict:
        url = jsonData['repository']['url']
    else:
        url = jsonData['repository']

    url = url.replace("git@github.com:", "")
    url = url.replace(".git", "")
    data['repository'] = url

    try:
        data['dependencies'] = list(jsonData['dependencies'].values())
    except:
        pass

    return str(data)

def get_repository(bytes_as_file)->str:
    json_as_string = zipLogic(bytes_as_file)
    jsonData = json.loads(json_as_string)

    url = ""
    if type(jsonData['repository']) is dict:
        url = jsonData['repository']['url']
    else:
        url = jsonData['repository']

    url = url.replace("git@github.com:", "")
    url = url.replace(".git", "")

    return url
    


@app.route('/home')
def homepage():

    return render_template('root.html')

@app.route('/home/reset')
def reset():

    return render_template('reset_warning.html')

@app.route('/home/reset-confirmed', methods=["GET", "POST"])
def resetConfirmed():
    if request.method == 'GET':
        return redirect('/home')
    gcs = storage.Client()

    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blobs = [blob_new.name for blob_new in bucket.list_blobs()] # List all the blobs available
    for target_name in blobs:
        target_blob = bucket.blob(target_name)  #Get the right blob by filename
        target_blob.delete()
    

    return render_template('reset_complete.html')

@app.route('/home/upload-package')
def uploadPackage():

    return render_template('upload_package.html')

@app.route('/home/download-package', methods=['POST'])
def downloadPackage():
    if request.method == 'POST':
        get_package_index = int(request.form['package_index'])

    gcs = storage.Client()

    # Get the bucket that the file will be downloaded from.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blobs = [blob_new.name for blob_new in bucket.list_blobs()] # List all the blobs available
    target_name =  blobs[get_package_index] #Get the blob name
    target_blob = bucket.blob(target_name)  #Get the right blob by filename
    bytes = target_blob.download_as_bytes()
    bytes_as_file = BytesIO(bytes)

    return send_file(bytes_as_file, as_attachment=True, attachment_filename=target_name)

@app.route('/home/view-packages', methods=['GET', 'POST'])
def viewPackages(curr_page = 1):
    if request.method == 'POST':
        curr_page = request.form['next_page']
    #print("CURR PAGE1: ", curr_page)
    try:
        curr_page = int(curr_page)
    except:
        curr_page = 1
    #print("CURR PAGE2: ", curr_page)
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
    #print("CURR PAGE3: ", curr_page)
    for  index_blobs, blob in enumerate(bucket.list_blobs(max_results=max_results)):
        if index_blobs >= ((curr_page-1) * MAX_RESULTS_PER_PAGE):
            #print("Blob index is: ",index_blobs, " with name ", blob.name, " on page ", page)
            blob_tuple = (index_blobs, blob.name)
            package_identifiers.append(blob_tuple)

    return render_template('view_packages.html', package_identifiers=package_identifiers, curr_page=curr_page, max_pages=max_pages)

@app.route('/home/upload', methods=['POST'])
def upload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in request.files:
            return redirect(request.url)
        uploaded_files = request.files.getlist('files')
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

        orig_data = uploaded_file.read()
        orig_contenttype = uploaded_file.content_type

        json_as_string = zipLogic(uploaded_file)
        fileID, fileName, fileVersion = makeIdentifiers(json_as_string)
        file_ID = fileID.replace("_", "")  #Ensure underscores are only used in the final filename
        file_name = fileName.replace("_", "")
        final_file_name = secure_filename(file_name + "_" + file_ID + "_" + fileVersion + ".zip")
        uploaded_file.filename = final_file_name

        # Create a new blob and upload the file's content.
        blob = bucket.blob(uploaded_file.filename)

        blob.upload_from_string(
            orig_data,
            content_type=orig_contenttype
        )
    return render_template('upload_package_success.html')

class APIHome(Resource):
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

class ViewPackages(Resource):
    def __init__(self):
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument('offset', type = int, default=1, location='args')

            
    def post(self):
        try:   
            input_json = request.get_json()   

            search_names = []
            search_versions = []
            print(input_json)
            queried = False
            if input_json is not None:
                queried = True
                for package_request in input_json:
                    try:
                        name = package_request.get('Name')
                        if name is None:
                            raise
                        search_names.append(name)
                    except:
                        print("name not present")
                        return {"message": "Error in request. Specific package requested but no name given with header 'Name'"}, 400
                    try:
                        version = package_request.get('Version')
                        if version is None:
                            raise
                        search_versions.append(version)
                    except:
                        print("version not present, defaulting to all versions")
                        search_versions.append("ALL_VERSIONS") #All versions if not given


            args = self.reqparse.parse_args()
            offset = int(args['offset']) #Should be int given by user
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
            #max_results = MAX_RESULTS_PER_PAGE * curr_page
            package_identifiers = []
            if queried:
                matching_packages_page = []
                results_found = 0
                for  index_blobs, blob in enumerate(bucket.list_blobs()):
                    fileName, fileID, fileVersion = blob.name.split('_')
                    fileVersion = fileVersion.replace(".zip", "")
                    try:
                        if (fileName in search_names) and (versionChecker(fileVersion, search_versions[search_names.index(fileName)]) ):

                            JsonIdentifier = {
                            "Name": fileName,
                            "Version": fileVersion,
                            "ID": fileID
                            }
                            package_identifiers.append(JsonIdentifier)
                            results_found += 1
                    except:
                        return {"message": "Version parsing error. Please check request for proper versioning notation."}, 400
                max_pages = round_up(results_found, MAX_RESULTS_PER_PAGE)
                if(curr_page > max_pages):
                    curr_page = max_pages
                for index, package_info in enumerate(package_identifiers):
                    if index >= ((curr_page-1) * MAX_RESULTS_PER_PAGE):
                        matching_packages_page.append(package_info)
                return matching_packages_page, 201

            else:
                for  index_blobs, blob in enumerate(bucket.list_blobs()):
                    if index_blobs >= ((curr_page-1) * MAX_RESULTS_PER_PAGE):
                        #print("Blob index is: ",index_blobs, " with name ", blob.name, " on page ", page)
                        
                        #blob_tuple = (index_blobs, blob.name)
                        #package_identifiers.append(blob_tuple)
                        fileName, fileID, fileVersion = blob.name.split('_') # get the metadata from the blob name
                        #fileVersion = fileVersion.removesuffix('.zip') # remove .zip from fileversion  #TODO Discuss with Mohamamd why "removesuffix" doesnt exist -> this was added in 3.9, use replace
                        fileVersion = fileVersion.replace(".zip", "")
                        JsonIdentifier = {
                        "Name": fileName,
                        "Version": fileVersion,
                        "ID": fileID
                        }
                        package_identifiers.append(JsonIdentifier)

                return package_identifiers, 201 #May need a "json.dumps()" here for package_identifiers since it is a list of JSONs
               
        except:
            return {"message": "Error in request."}, 400


class UploadPackage(Resource):
    def post(self):
        try:
            # Get the bucket that the file will be uploaded to.
            gcs = storage.Client()
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            # Read payload as json
            input_json = request.get_json()

            file_name = str(input_json['metadata']['Name'])
            file_ID = str(input_json['metadata']['ID'])
            file_version = str(input_json['metadata']['Version'])
            file_ID = file_ID.replace("_", "")  #Ensure underscores are only used in the final filename
            file_name = file_name.replace("_", "")
            final_file_name = secure_filename(file_name + "_" + file_ID + "_" + file_version + ".zip") #Set filename for storage on GCP (Storage and SQL)
            
            # Create a new blob and upload the file's content.
            blob = bucket.blob(final_file_name)

            # if package already exists 
            if blob.exists():
                return {"message":"Package already exists."}, 403

            # if ID already being used by another package
            for presentBlob in bucket.list_blobs():
                if "_" + file_ID + "_" in presentBlob.name:
                    return {"message":"Package ID already taken."}, 403


            # Upload by package Create or Ingestion
            if 'Content' in input_json['data']:
                # parse the metadata and data fields in the request
                file_string = input_json['data']['Content']

                decoded_data = base64.b64decode(bytes(file_string, 'utf-8')) # Make into bytes
                uploaded_file = BytesIO(decoded_data)

                blob.upload_from_string(uploaded_file.read(), content_type='application/zip')
            elif 'URL' in input_json['data']:
                extraMain = "/zipball/main"
                extraMaster = "/zipball/master"
                r = requests.get(input_json['data']['URL'] + extraMain)

                if r.status_code != 200:
                    r = requests.get(input_json['data']['URL'] + extraMaster)

                if r.status_code != 200:
                    return {"message":"URL not supported. Package not ingestible."}, 400

                decoded_data = r.content
                uploaded_file = BytesIO(decoded_data)
                json_as_string = zipLogic(uploaded_file)
                
                try:
                    output = subprocess.run(["./Java_install/jdk-17.0.1/bin/java", "-jar", "trustworthiness_copy-1.0-SNAPSHOT-jar-with-dependencies.jar", format_json_string(json_as_string)], capture_output=True)
                except:
                    return {"message":"Malformed request. It is either package.json does not exist or does not contain a repository field"}, 400

                try:    
                    output_json =  output.stdout.decode("utf-8")
                    data = json.loads(output_json)['Scores'][0]
                    print(data)

                    if data['busFactor'] >= 0.5 and data['correctnessScore'] >= 0.5 and data['rampUpTimeScore'] >= 0.5 and data['responsivenessScore'] >= 0.5 and data['licenseScore'] >= 0.5 and data['dependencyRatio'] >= 0.5:
                        blob.upload_from_string(decoded_data, content_type='application/zip')
                    else:
                        return {"message":"Package is not ingestible. One or more scores less than 0.5."}, 400
                except:
                    return {"message":"Package is not ingestible. The rating system choked so could not validate URL scores"}, 400
            else:
                return {"message":"Malformed request."}, 400
            
            responseJson = {
                "Name": file_name,
                "Version": file_version,
                "ID": file_ID
            }

            return responseJson, 201
        except:
            return {"message":"Malformed request."}, 400

class HandlePackageByName(Resource):
    def get(self, packageName):
        #TODO - retrieve all the package versions.
        pass

    def delete(self, packageName):
        try:
            gcs = storage.Client()
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            target_blob = [blob.name for blob in bucket.list_blobs() if blob.name.startswith(packageName)] # List all the blobs available

            if target_blob == []:
                return {"message": "No such Package."}, 400

            for target_name in target_blob:
                target_blob = bucket.blob(target_name)  # Get the right blob by filename
                target_blob.delete()

            return {"message": "Package is deleted."}, 200
        except:
            return {"message": "Error in request."}, 400

class HandlePackageById(Resource):
    def get(self, packageId):
        response = {
                "code": -1,
                "message": "An error occurred while retrieving package"
        }

        try:
            gcs = storage.Client()
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            for blob in bucket.list_blobs():
                if "_" + packageId + "_" in blob.name:
                    bytes_as_file = BytesIO(blob.download_as_bytes())
                    fileName, fileId, fileVersion = blob.name.split('_') # get the metadata from the blob name
                    fileVersion = fileVersion.replace(".zip", "")

                    packageContent = base64.b64encode(bytes_as_file.read())
                    packageContentString = packageContent.decode('ascii')

                    response = {
                        "metadata": {
                            "Name": fileName,
                            "Version": fileVersion,
                            "ID": fileId
                        },
                        "data": {
                            "Content": packageContentString,
                            "URL": "https://github.com/" + get_repository(bytes_as_file),
                            "JSProgram": "This field is currently not supported by our API"
                        }
                    }
                    return response, 200
            return response, 500
        except:
            return response, 500 

    def put(self, packageId):
        try:
            # Get the bucket that the file will be uploaded to.
            gcs = storage.Client()
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            # Read payload as json
            input_json = request.get_json()

            # parse the metadata and data fields in the request
            file_name = str(input_json['metadata']['Name'])
            file_ID = str(input_json['metadata']['ID'])
            file_version = str(input_json['metadata']['Version'])
            final_file_name = file_name + "_" + file_ID + "_" + file_version + ".zip" #Set filename for storage on GCP (Storage and SQL)
            final_file_name = secure_filename(final_file_name) #Set filename for storage on GCP (Storage and SQL)

            if file_ID != packageId:
                return {"message":"package ID in metadata does not match package ID in request."}, 400

            for blob in bucket.list_blobs():
                if blob.name == final_file_name:
                    if 'Content' in input_json['data']:
                        file_string = input_json['data']['Content']
                        decoded_data = base64.b64decode(bytes(file_string, 'utf-8')) #Make into bytes
                        uploaded_file = BytesIO(decoded_data)

                        # get blob and update the file's content.
                        blob = bucket.get_blob(final_file_name)
                        blob.upload_from_string(uploaded_file.read(), content_type='application/zip')
                    elif 'URL' in input_json['data']:
                        extraMain = "/zipball/main"
                        extraMaster = "/zipball/master"
                        r = requests.get(input_json['data']['URL'] + extraMain)

                        if r.status_code != 200:
                            r = requests.get(input_json['data']['URL'] + extraMaster)

                        if r.status_code != 200:
                            return {"message":"URL not supported. Update unsuccessful."}, 400

                        decoded_data = r.content
                        uploaded_file = BytesIO(decoded_data)
                        json_as_string = zipLogic(uploaded_file)

                        try:
                            output = subprocess.run(["./Java_install/jdk-17.0.1/bin/java", "-jar", "trustworthiness_copy-1.0-SNAPSHOT-jar-with-dependencies.jar", format_json_string(json_as_string)], capture_output=True)
                        except:
                            return {"message":"Malformed request. It is either package.json does not exist or does not contain a repository field"}, 400
                        
                        try:
                            output_json =  output.stdout.decode("utf-8")
                            data = json.loads(output_json)['Scores'][0]
                            
                            if data['busFactor'] >= 0.5 and data['correctnessScore'] >= 0.5 and data['rampUpTimeScore'] >= 0.5 and data['responsivenessScore'] >= 0.5 and data['licenseScore'] >= 0.5 and data['dependencyRatio'] >= 0.5:
                                # get blob and update the file's content.
                                blob = bucket.get_blob(final_file_name)
                                blob.upload_from_string(uploaded_file.read(), content_type='application/zip')
                            else:
                                return {"message":"Update unsuccessful. One or more scores less than 0.5."}, 400
                        except:
                            return {"message":"Update unsuccessful. The rating system choked so could not validate URL scores"}, 400
                    else:
                        return {"message":"Malformed request."}, 400
                    return "", 200
            return {"message":"No such package exists."}, 400
        except:
            return {"message":"Malformed request."}, 400

    def delete(self, packageId):
        try:
            gcs = storage.Client()
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            target_blob = [blob.name for blob in bucket.list_blobs() if "_" + packageId + "_" in blob.name] # List all the blobs available

            if target_blob == []:
                return {"message": "No such Package."}, 400

            for target_name in target_blob:
                target_blob = bucket.blob(target_name)  # Get the right blob by filename
                target_blob.delete()

            return {"message": "Package is deleted."}, 200
        except:
            return {"message": "Error in request."}, 400

class Rates(Resource):
    def get(self, packageId):
        try:
            # connect to cloud storage
            gcs = storage.Client()
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            # loop through all the files in the bucket to find the package of interest
            for blob in bucket.list_blobs():
                if "_" + packageId + "_" in blob.name:
                    bytes_as_file = BytesIO(blob.download_as_bytes())
                    json_as_string = zipLogic(bytes_as_file)

                    # use this if you are deploying
                    output = subprocess.run(["./Java_install/jdk-17.0.1/bin/java", "-jar", "trustworthiness_copy-1.0-SNAPSHOT-jar-with-dependencies.jar", format_json_string(json_as_string)], capture_output=True)
                    output_json =  output.stdout.decode("utf-8")
                    data = json.loads(output_json)['Scores'][0]

                    response = {
                        "BusFactor": data['busFactor'],
                        "Correctness": data['correctnessScore'],
                        "RampUp": data['rampUpTimeScore'],
                        "ResponsiveMaintainer": data['responsivenessScore'],
                        "LicenseScore": data['licenseScore'],
                        "GoodPinningPractice": data['dependencyRatio']
                    }
                    return response, 200

            return {"message":"No such package exists."}, 400
        except:
            return {"message":"The package rating system choked on at least one of the metrics."}, 500

class RegistryReset(Resource):
    def delete(self):
        try:
            gcs = storage.Client()
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            blobs = [blob_new.name for blob_new in bucket.list_blobs()] # List all the blobs available
            for target_name in blobs:
                target_blob = bucket.blob(target_name)  # Get the right blob by filename
                target_blob.delete()

            return {"description": "Registry is reset"}, 200
        except:
            return {"description": "Error in return"}, 400

api.add_resource(APIHome, '/')
api.add_resource(ViewPackages, '/packages')
api.add_resource(UploadPackage, '/package')
api.add_resource(HandlePackageByName, '/package/byName/<string:packageName>')
api.add_resource(HandlePackageById, '/package/<string:packageId>')
api.add_resource(Rates, '/package/<string:packageId>/rate')
api.add_resource(RegistryReset, '/reset')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
