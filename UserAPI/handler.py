import pymysql
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Configuration Values
endpoint = 'jmtgr.cij2xpo0vglc.us-east-1.rds.amazonaws.com'
username = 'multicampusjmtgr'
password = 'JMtgr1117'
database_name = 'jmtgrtest'

#Connection
connection = pymysql.connect(endpoint, user=username,
                passwd=password, db=database_name, charset='utf8')

#User Insert / Select List - snchoi
def handler(event, context):
    print(event)
    operation = event['httpMethod']
    if operation == 'GET':
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * from USER')
        rows = cursor.fetchall()
        return {
            "statusCode":200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps(rows)
        }
    elif operation == 'POST':
        print(event)
        body = json.loads(event['body'])
        print(body)
        email = body['email']
        interest = body['interest']
        name = body['name']
        phone_number = body['phone_number']
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "INSERT INTO USER VALUES ('{}','{}','{}','{}')".format(email, interest, name, phone_number)
        # print('query : ', query)
        result = cursor.execute(query)
        if result == 1:
            connection.commit()
            return {
                "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                        # "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                        "Access-Control-Allow-Credentials": "true"
                    },
                "statusCode":200,
                "body":True
            }
        return {
            "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                        # "Access-Control-Allow-Headers": "Content-Type",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                        "Access-Control-Allow-Credentials": "true"
                    },
            "statusCode":400,
            "body":False
        }
    