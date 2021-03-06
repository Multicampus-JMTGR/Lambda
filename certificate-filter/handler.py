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
    """
    MYSQL RDS 쿼리 부분
    """
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        print(event)
        
        keyword = event['queryStringParameters']['keyword']
        print(keyword)
        
        cur.execute(f"SELECT * FROM CERTIFICATE \
                     WHERE name LIKE '%{keyword}%'")
        
        # cur.execute(f"SELECT * FROM CERTIFICATE \
        #             WHERE name LIKE '%{event['keyword']}%'")
                
        rows = cur.fetchall()
        return {
            "statusCode":200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": "true"
            },
            "body": json.dumps(rows)
        }