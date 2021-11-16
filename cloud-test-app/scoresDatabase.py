import os
import psycopg2
import psycopg2.extras
import json
import pymysql

def parseJson(filename:str)->dict:
    with open(filename) as json_file:
        data = json.load(json_file)

    return data

def main(filename):
    try:
        data = parseJson(filename)
        db_user = os.environ['CLOUD_SQL_USERNAME']
        db_password = os.environ['CLOUD_SQL_PASSWORD']
        db_name = os.environ['CLOUD_SQL_DATABASE_NAME']
        db_connection_name = os.environ['CLOUD_SQL_CONNECTION_NAME']
        db_address = os.environ['CLOUD_SQL_IP']
        db_port = os.environ['CLOUD_SQL_CONNECTION_PORT']
            # conn = connecttoDB()
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            conn = pymysql.connect(unix_socket=unix_socket, db=db_name, user=db_user, password=db_password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        else:
            conn = pymysql.connect(host=db_address, db=db_name, user=db_user, password=db_password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        with conn:
            with conn.cursor() as cursor:
                for entry in data["scores"]:
                    cursor.execute("INSERT INTO scores_table (url, ramp_up_score, correctness_score, bus_factor_score, responsive_maintainer_score, license_score, dependency_score) VALUES(%s, %s, %s, %s, %s, %s, %s)", (entry["url"], entry["rampup"], entry["correctness"], entry["busfactor"], entry["contributors"], entry["license"], entry["dependency"]))
            
        conn.close()
    except:
        pass

if __name__ == "__main__":
    main()
