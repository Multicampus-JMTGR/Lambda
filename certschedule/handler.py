import sys
import logging
import pymysql
import os
import json
import datetime

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
    
    def datetime_handler(x):
        if isinstance(x, datetime.date):
            return x.isoformat()
        raise TypeError("Unknown type")
    
    
    month = event['queryStringParameters']['month']
    
    """
    MYSQL RDS 쿼리 부분
    """
    with conn.cursor() as cur:
        cur.execute(f"SELECT reg_start_date, reg_end_date, test_start_date, test_end_date, result_date_1, result_date_2, test_type, \
        CERTIFICATE.cert_id, CERTIFICATE.name, department, pass_percent, pass_percent_sil, cost, cost_sil, examinee, examinee_sil, link \
        FROM CERT_SCHEDULE \
        INNER JOIN CERTIFICATE ON CERT_SCHEDULE.cert_id_id = CERTIFICATE.cert_id \
        WHERE MONTH(reg_start_date) = {month} OR MONTH(reg_end_date) = {month} OR MONTH(test_start_date) = {month} OR MONTH(test_end_date) = {month} OR MONTH(result_date_1) = {month} OR MONTH(result_date_2) = {month}"
        )
        
        r = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    
        
        #return json.loads(json.dumps(r, default=datetime_handler))
        
        return {
                "statusCode":200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "http://jmtgr.s3-website-us-east-1.amazonaws.com",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    "Access-Control-Allow-Credentials": "true"
                },
                "body": json.dumps(r, default=datetime_handler)
            }