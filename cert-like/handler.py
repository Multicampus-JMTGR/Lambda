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

    user_id = event['user_id']
    certificate_id = int(event['certificate_id'])
    print(user_id)
    print(certificate_id)
    
    """
    MYSQL RDS 쿼리 부분
    """
    
    
    with conn.cursor() as cur:
        # query = "INSERT INTO USER_cert_likes (user_id, certificate_id) VALUES ('aaaa@naver.com', 30)"
        # print(query)
        # result = cur.execute(query)
        cur.execute("SELECT * FROM USER_cert_likes")
        rows = cur.fetchall()

        for row in rows:
            print(user_id, type(user_id), certificate_id, type(certificate_id), row[1], type(row[1]), row[2], type(row[2]))
            # 만약 좋아요가 이미 존재 한다면 삭제하고 삭제된 row return
            if row[1] == user_id and row[2] == certificate_id:
                cur.execute("DELETE FROM USER_cert_likes \
                            WHERE user_id = '{}' and certificate_id= '{}'".format(event['user_id'], event['certificate_id']))
                conn.commit()
                print ("deleted")
                return ("deleted")
        
        # 못찾았다면 row insert
        cur.execute("INSERT INTO USER_cert_likes (user_id, certificate_id) VALUES ('{}', '{}')".format(event['user_id'], event['certificate_id']))
        conn.commit()
        print("inserted")
        return (event['user_id'], event['certificate_id'])