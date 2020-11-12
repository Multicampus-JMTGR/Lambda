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
    with conn.cursor() as cur:

        cur.execute("SELECT * FROM USER_cert_likes")
                
        rows = cur.fetchall()
        # for row in rows:
        #     for i in range(len(row)):
        #         print(row[0])
        return rows