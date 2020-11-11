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
        cur.execute("SELECT schedule_id, test_round, test_type, \
                    reg_start_date, reg_end_date, test_start_date, test_end_date, result_date_1, result_date_2, \
                    CERTIFICATE.cert_id, CERTIFICATE.name, department, pass_percent, pass_percent_sil, cost, cost_sil, examinee, examinee_sil, link \
                    FROM CERT_SCHEDULE \
                    INNER JOIN CERTIFICATE ON CERT_SCHEDULE.cert_id = CERTIFICATE.cert_id \
                    WHERE MONTH(reg_start_date) = 5 OR MONTH(reg_end_date) = 5 OR MONTH(test_start_date) = 5 OR MONTH(test_end_date) = 5 OR MONTH(result_date_1) = 5 OR MONTH(result_date_2) = 5"
                    )
        rows = cur.fetchall("SELECT ")
        return rows