import pymysql, json, datetime
import re
import boto3

#Configuration Values
endpoint = 'jmtgr.cij2xpo0vglc.us-east-1.rds.amazonaws.com'
username = 'multicampusjmtgr'
password = 'JMtgr1117'
database_name = 'jmtgrtest'

#Connection
connection = pymysql.connect(endpoint, user=username, passwd=password, db=database_name, charset='utf8')

def lambda_handler(event, context):
    cursor = connection.cursor()
    
    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        else:
            return value
#             raise TypeError('not JSON serializable')

    # CERTIFICATE 와 CERT_SCHEDULE 을 inner join 하여 필요한 데이터만 추출
    cursor.execute('select CERTIFICATE.cert_id, CERTIFICATE.name, \
                    CERT_SCHEDULE.test_type, CERT_SCHEDULE.test_round, CERT_SCHEDULE.test_start_date \
                    from CERT_SCHEDULE \
                    INNER JOIN CERTIFICATE \
                    on CERT_SCHEDULE.cert_id_id = CERTIFICATE.cert_id \
                    where(test_start_date = date(subdate(now(), INTERVAL -11 DAY)))')
    cert_join = []
    cert_join = cursor.fetchall()
    # cursor.close()
#     ensure_ascii = False ==> json.dumps 이용시 한글이 유니코드로 저장되는 것을 방지
#     default=json_default ==> json 모듈 사용시 not JSON serializable 에러를 피하는 방법
#                             json.dumps 과정에서 json 모듈이 알아들을 수 없는 것들이 들어가는 경우
#                             가장 대표적인 예가 바로 python 날짜/시간 타입을 곧이 곧대로 넣었을 경우
    cert_join_json = json.dumps(cert_join, ensure_ascii = False, default=json_default, indent=4)
    
    cert_join_py = json.loads(cert_join_json)
#     print(cert_join_py)

    # USER_cert_likes 테이블을 위에서 추출한 데이터와 비교
    cursor = connection.cursor()
    cursor.execute('select user_id, certificate_id \
                    from USER_cert_likes')
                    
    user_like = []
    user_like = cursor.fetchall()
    # cursor.close()
#     ensure_ascii = False ==> json.dumps 이용시 한글이 유니코드로 저장되는 것을 방지
#     default=json_default ==> json 모듈 사용시 not JSON serializable 에러를 피하는 방법
#                             json.dumps 과정에서 json 모듈이 알아들을 수 없는 것들이 들어가는 경우
#                             가장 대표적인 예가 바로 python 날짜/시간 타입을 곧이 곧대로 넣었을 경우
#     intent=4 ==> 4만큼 들여쓰기, 가독성향상
    user_like_json = json.dumps(user_like, ensure_ascii = False, default=json_default, indent=4)
    
    user_like_py = json.loads(user_like_json)
#     print(user_like_py)
    
    data_list = []
    for ul_data in user_like_py:
        for cj_data in cert_join_py:
            if ul_data[1] == cj_data[0]:
                # 이것도 가능. email주소가 뒤에 붙음
#                 cj_data.append(ul_data[0])
#                 data_list.append(cj_data)

                temp = []
                temp.append(ul_data[0])
                temp.extend(cj_data)
                data_list.append(temp)
    # print(f"result: {data_list}")
    
    if not data_list:
        return 'no data'
    else:
        return data_list
        # return json.dumps(data_list[0], ensure_ascii = False, default=json_default)