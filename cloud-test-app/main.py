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

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
MAX_RESULTS_PER_PAGE = 10
ALLOWED_EXTENSIONS = {'zip'}

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

def format_json_string(json_as_string)->str:
    jsonData = json.loads(json_as_string)
    data = {}
    data['repository'] = jsonData['repository']
    try:
        data['dependencies'] = list(jsonData['dependencies'].values())
        data['dependencies'] = [s.replace("^", "") for s in data['dependencies']]
    except:
        pass

    return str(data)

def get_repository(bytes_as_file)->str:
    json_as_string = zipLogic(bytes_as_file)
    jsonData = json.loads(json_as_string)

    return jsonData['repository']

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

class UploadPackage(Resource):
    def post(self):
        try:
            # Get the bucket that the file will be uploaded to.
            gcs = storage.Client()
            bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

            # Read payload as json
            input_json = request.get_json()

            # parse the metadata and data fields in the request
            file_string = input_json['data']['Content']
            file_name = str(input_json['metadata']['Name'])
            file_ID = str(input_json['metadata']['ID'])
            file_version = str(input_json['metadata']['Version'])

            final_file_name = secure_filename(file_name + "_" + file_ID + "_" + file_version + ".zip") #Set filename for storage on GCP (Storage and SQL)
            decoded_data = base64.b64decode(bytes(file_string, 'utf-8')) #Make into bytes
            

            uploaded_file = BytesIO(decoded_data)
            # Create a new blob and upload the file's content.
            blob = bucket.blob(final_file_name)

            # if package already exists 
            if blob.exists():
                return {"message":"Package already exists."}, 403

            # if ID already being used by another package
            for blob in bucket.list_blobs():
                 if "_" + file_ID + "_" in blob.name:
                     return {"message":"Package ID already taken."}, 403

            blob.upload_from_string(uploaded_file.read(), content_type='application/zip')
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
                    fileVersion = fileVersion.removesuffix('.zip') # remove .zip from fileversion

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
            file_string = input_json['data']['Content']
            file_name = str(input_json['metadata']['Name'])
            file_ID = str(input_json['metadata']['ID'])
            file_version = str(input_json['metadata']['Version'])

            if file_ID != packageId:
                return {"message":"Malformed request."}, 400

            final_file_name = file_name + "_" + file_ID + "_" + file_version + ".zip" #Set filename for storage on GCP (Storage and SQL)
            decoded_data = base64.b64decode(bytes(file_string, 'utf-8')) #Make into bytes
            uploaded_file = BytesIO(decoded_data)

            # get blob and update the file's content.
            blob = bucket.get_blob(final_file_name)
            blob.upload_from_string(uploaded_file.read())

            return "",200
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

                    output = subprocess.run(["java", "-jar", "trustworthiness_copy-1.0-SNAPSHOT-jar-with-dependencies.jar", format_json_string(json_as_string)], capture_output=True)

                    # use this if you are deploying
                    # output = subprocess.run(["./Java_install/jdk-17.0.1/bin/java", "-jar", "trustworthiness_copy-1.0-SNAPSHOT-jar-with-dependencies.jar", format_json_string(json_as_string)], capture_output=True)
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
            return {"message":"The package rating system chocked on at least one of the metrics."}, 500

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
api.add_resource(UploadPackage, '/package')
api.add_resource(HandlePackageByName, '/package/byName/<string:packageName>')
api.add_resource(HandlePackageById, '/package/<string:packageId>')
api.add_resource(Rates, '/package/<string:packageId>/rate')
api.add_resource(RegistryReset, '/reset')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
