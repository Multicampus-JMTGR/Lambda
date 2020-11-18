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


# ToDoList - GET
def handler(event, context):
    def datetime_handler(x):
        if isinstance(x, datetime.date):
            return x.isoformat()
        raise TypeError("Unknown type")
        
    
    operation = event['httpMethod']
    
    # ToDoList 조회
    if operation == 'GET':
        # cert_id = event['pathParameters']['cert_id']
        email = event['pathParameters']['email']
        
        cursor = connection.cursor()
        # query = 'select * from STUDY_PLAN sp inner join CERTIFICATE C on sp.cert_id = C.cert_id \
        # inner join CERT_SCHEDULE CS on C.cert_id = CS.cert_id_id \
        # where C.cert_id={} and sp.email_id="{}"'.format(cert_id, email)
        query = "SELECT * FROM STUDY_PLAN  WHERE STUDY_PLAN.email_id = '{}'".format(email)
        print('query : ', query)
        cursor.execute(query)

        r = [dict((cursor.description[i][0], value) \
              for i, value in enumerate(row)) for row in cursor.fetchall()]
        
        return {
            "statusCode":200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": "true"
            },
            "body":json.dumps(r, default=datetime_handler)
        }
        
    # ToDoList 삽입
    elif operation == 'POST':
        body = json.loads(event['body'])
        contents = body['contents']
        cert_id = body['cert_id']
        email = body['email']
        
        dt = datetime.datetime.now()
        now_date = dt.strftime("%Y-%m-%d")
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "insert into STUDY_PLAN value (0,'{}','{}',{}, '{}')".format(now_date, contents, cert_id, email)
        result = cursor.execute(query)
        if result:
            connection.commit()
            return {
                "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": "true"
                },
                "statusCode":200,
                "body":True
            }
        return {
            "statusCode":400,
            "body": False
        }
    
    # ToDoList 삭제
    elif operation == "DELETE":
        content = event['queryStringParameters']['content']
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "delete from STUDY_PLAN where content = {}".format(content)
        result = cursor.execute(query)
        if result:
            connection.commit()
            return {
                "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": "true"
                },
                "statusCode":200,
                "body":True
            }
        return {
            "statusCode":400,
            "body": False
        }
