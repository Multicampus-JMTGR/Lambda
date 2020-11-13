import pymysql
import json

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
    print('event : ', event)
    operation = event['httpMethod']
    email = event['pathParameters']['email']
    print('email : ', email)
    
    if operation == 'GET':
        
        main_dict = {}
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        # 사용자 정보
        cursor.execute('SELECT * from USER where email="{}"'.format(email))
        rows = cursor.fetchall()
        main_dict = rows[0]
        
        # 사용자가 누른 좋아요 정보
        cursor.execute('SELECT id, certificate_id from USER_cert_likes where user_id="{}"'.format(email))
        rows_likes = cursor.fetchall()
        main_dict['cert_likes'] = rows_likes
        
        
        return {
            "statusCode":200,
            "headers":{"Content-Type":"application.json"},
            "body":json.dumps(main_dict)
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
    
