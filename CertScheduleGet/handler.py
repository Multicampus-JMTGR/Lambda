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


# 특정 자격증 스케줄 조
def handler(event, context):
    
    def datetime_handler(x):
        if isinstance(x, datetime.date):
            return x.isoformat()
        raise TypeError("Unknown type")
    
    operation = event['httpMethod']
    cert_id = event['pathParameters']['cert_id']

    
    if operation == 'GET':
        cur = connection.cursor()
        # 사용자 정보
        cur.execute('select * from CERT_SCHEDULE where cert_id_id={}'.format(cert_id))
        rows = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
        
        return {
            "statusCode":200,
            "headers": {
            "Content-Type":"application/json",
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Credentials": "true"
            },
            "body": json.dumps(rows, default=datetime_handler)
        }
        
  