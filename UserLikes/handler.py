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

    
    if operation == 'GET':
        main_dict = {}
        test_dict = {}
        sub_list = []
        
        
        cur = connection.cursor()
        # 사용자 정보
        cur.execute('SELECT * from USER WHERE email="{}"'.format(email))
        rows = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
        main_dict = rows[0]
        
        # 사용자가 누른 좋아요 정보
        cur.execute('SELECT * from USER_cert_likes where user_id="{}"'.format(email))
        rows_likes = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
        test_dict['cert_likes'] = rows_likes
        #print('main_dict : ', main_dict)
        
        # 좋아요 누른 자격증 스케쥴 정보
        for cert_like in test_dict['cert_likes']:
            cert_dict = {}
            #print(cert_like['certificate_id'])
            cert_id = cert_like['certificate_id']
            cur.execute('SELECT * from CERTIFICATE where cert_id="{}"'.format(cert_id))
            rows_likes_certificate = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
            cert_dict = rows_likes_certificate[0]
            print('cert_dict : ', cert_dict)
            
            
            cur.execute('select * from CERT_SCHEDULE where cert_id_id="{}"'.format(cert_id))
            
            rows_likes_certschedule = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
            
            #rows_likes_certschedule = cur.fetchall()
            print('rows_likes_certschedule : ', json.dumps(rows_likes_certschedule, default=datetime_handler))
            cert_dict['cert_schedule'] = rows_likes_certschedule
            print('cert_dict : ', cert_dict)
            
            sub_list.append(cert_dict)
            main_dict['cert_likes'] = sub_list
            
        print('main_dict : ', main_dict)
        
        
        return {
            "statusCode":200,
            "headers": {
            "Content-Type":"application.json",
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps(main_dict, default=datetime_handler)
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
    
