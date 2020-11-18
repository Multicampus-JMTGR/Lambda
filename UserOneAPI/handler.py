import pymysql
import json
import datetime

#Configuration Values
endpoint = 'jmtgr.cij2xpo0vglc.us-east-1.rds.amazonaws.com'
username = 'multicampusjmtgr'
password = 'JMtgr1117'
database_name = 'jmtgrtest'

#Connection
connection = pymysql.connect(endpoint, user=username,
                passwd=password, db=database_name, charset='utf8')


# User Select One - 회원 존재 유무 확인 , User Update - 회원 수정 / 로그인 시 기존회원인 경우 update
def handler(event, context):
    
    def datetime_handler(x):
        if isinstance(x, datetime.date):
            return x.isoformat()
        raise TypeError("Unknown type")
    
    operation = event['httpMethod']
    email = event['pathParameters']['email']

    print(operation, email)
    
    if operation == 'GET':
        print(">>> GET")
        cur = connection.cursor(pymysql.cursors.DictCursor)
        # 사용자 정보
        connection.commit()
        cur.execute('select * from USER where email="{}"'.format(email))
        rows = cur.fetchone()
        print(rows)
        
        if rows == None:
            return {
                "statusCode":400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    "Access-Control-Allow-Credentials": "true"
                }
            }
        else :
            return {
                "statusCode":200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    "Access-Control-Allow-Credentials": "true"
                },
                "body": json.dumps(rows, default=datetime_handler)
            }
        
        
    elif operation == 'PUT':
        body = json.loads(event['body'])
        interest = body['interest']
        name = body['name']
        phone_number = body['phone_number']
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "UPDATE USER SET interest = '{}', name = '{}', phone_number = '{}' WHERE email='{}'".format(interest, name, phone_number, email)
        print('query : ', query)
        result = cursor.execute(query)
        print('result : ', result)
        if result:
            connection.commit()
            return {
                "statusCode":200,
                "body":True
            }
        return {
            "statusCode":400,
            "body": False
        }
    
