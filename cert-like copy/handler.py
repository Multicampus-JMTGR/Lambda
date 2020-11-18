import sys
import logging
import pymysql
import json
import os
from datetime import date, datetime

region = os.environ['AWS_REGION']


endpoint = 'jmtgr.cij2xpo0vglc.us-east-1.rds.amazonaws.com'
username = 'multicampusjmtgr'
password = 'JMtgr1117'
database_name = 'jmtgrtest'
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

conn = pymysql.connect(host=endpoint, port=port, db=database_name, user=username,
                passwd=password, charset='utf8')


def handler(event, context):
    
    body = json.loads(event['body'])
    user_id = body['email']
    certificate_id = body['cert_id']
    # user_id = "kmj1995kr@gmail.com"
    # certificate_id = 28
    print(user_id)
    print(certificate_id)
    
    """
    MYSQL RDS 쿼리 부분
    """
    
    
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute("SELECT * FROM USER_cert_likes")
        rows = cur.fetchall()
        print (rows)

        for row in rows:
            print(user_id, type(user_id), certificate_id, type(certificate_id), row['id'], type(row['id']), row['certificate_id'], type(row['certificate_id']))
            # 만약 좋아요가 이미 존재 한다면 삭제하고 삭제된 row return
            if row['user_id'] == user_id and row['certificate_id'] == certificate_id:
                cur.execute("DELETE FROM USER_cert_likes \
                            WHERE user_id = '{}' and certificate_id= '{}'".format(user_id, certificate_id))
                conn.commit() 
                
                cur.execute("SELECT id, user_id, certificate_id, name FROM USER_cert_likes \
                            INNER JOIN CERTIFICATE ON USER_cert_likes.certificate_id = CERTIFICATE.cert_id \
                            WHERE user_id='{}'".format(user_id))
                r = cur.fetchall()
                cur.close()
                print ("deleted")
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


        
        # 못찾았다면 row insert
        cur.execute("INSERT INTO USER_cert_likes (user_id, certificate_id) VALUES ('{}', {})".format(user_id, certificate_id))
        conn.commit()
        
        cur.execute("SELECT id, user_id, certificate_id, name FROM USER_cert_likes \
                    INNER JOIN CERTIFICATE ON USER_cert_likes.certificate_id = CERTIFICATE.cert_id \
                    WHERE user_id='{}'".format(user_id))
        r = cur.fetchall()
        cur.close()
        print("inserted")
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