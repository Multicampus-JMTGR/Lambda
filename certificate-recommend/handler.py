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


# 사용자가 좋아요 한 자격증 정
def handler(event, context):
    
    # operation = event['httpMethod']
    email = event['pathParameters']['email']

    #if operation == 'GET':
    with connection.cursor(pymysql.cursors.DictCursor) as cur:
    #cur = connection.cursor(pymysql.cursors.DictCursor)
    # 사용자 정보
        connection.commit()
        cur.execute("SELECT C.cert_id, C.name FROM USER_cert_likes Ucl \
                    INNER JOIN CERTIFICATE C ON Ucl.certificate_id = C.cert_id \
                    WHERE user_id='{}'".format(email))
        rows = cur.fetchall()
    
        # cur.execute("select C.cert_id, C.name from USER U inner join USER_cert_likes Ucl on U.email = Ucl.user_id \
        #             inner join CERTIFICATE C on Ucl.certificate_id = C.cert_id \
        #             where U.email='{}'".format(email))
        # rows = cur.fetchall()
        cur.close()
        return {
            "statusCode":200,
            "headers": {
                "Content-Type":"application/json",
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": "true"
            },
            "body": json.dumps(rows)
        }