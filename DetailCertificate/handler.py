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

connection = pymysql.connect(host=endpoint, port=port, db=database_name, user=username,
                passwd=password, charset='utf8')


def handler(event, context):
    cert_id = event['pathParameters']['cert_id']
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * from CERTIFICATE where cert_id = {}'.format(cert_id))
    rows = cursor.fetchall()
    return {
        "statusCode":200,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(rows)
    }
