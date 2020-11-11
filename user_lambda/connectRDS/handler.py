import pymysql

#Configuration Values
endpoint = 'jmtgr.cij2xpo0vglc.us-east-1.rds.amazonaws.com'
username = 'multicampusjmtgr'
password = 'JMtgr1117'
database_name = 'jmtgrdb'

#Connection
connection = pymysql.connect(endpoint, user=username,
                passwd=password, db=database_name, charset='utf8')

#User Insert / Select List - snchoi
def UserAPI(event, context):
    operation = event.httpMethod
    if operation == 'GET':
        cursor = connection.cursor()
        cursor.execute('SELECT * from USER')
        rows = cursor.fetchall()
        # for row in rows:
        #     print("{0} {1} {2}".format(row[0], row[1], row[2]))
        return rows    
    elif operation == 'POST':
        email = event['email']
        interest = event['interest']
        name = event['name']
        phone_number = event['phone_number']
        
        cursor = connection.cursor()
        query = "INSERT INTO USER VALUES ('{}','{}','{}','{}')".format(email, interest, name, phone_number)
        print('query : ', query)
        cursor.execute(query)
        connection.commit()
        return "성공"
    

# User Select One - 회원 존재 유무 확인 , User Update - 회원 수정 / 로그인 시 기존회원인 경우 update
def UserOneAPI(event, context):
    operation = event.httpMethod
    email = event["queryStringParameters"]["email"]
    if operation == 'GET':
        cursor = connection.cursor()
        cursor.execute('SELECT * from USER where email="{}"').format(email)
        rows = cursor.fetchall()
        # for row in rows:
        #     print("{0} {1} {2}".format(row[0], row[1], row[2]))
        return rows    
    elif operation == 'PUT':
        email = event['email']
        interest = event['interest']
        name = event['name']
        phone_number = event['phone_number']
        
        cursor = connection.cursor()
        query = "INSERT INTO USER VALUES ('{}','{}','{}','{}')".format(email, interest, name, phone_number)
        print('query : ', query)
        cursor.execute(query)
        connection.commit()
        return "성공"


# User Select One - 회원 존재 유무 확인 , User Update - 회원 수정 / 로그인 시 기존회원인 경우 update
def UserOneAPI(event, context):
    operation = event.httpMethod
    email = event["queryStringParameters"]["email"]
    if operation == 'GET':
        cursor = connection.cursor()
        cursor.execute('SELECT * from USER where email="{}"').format(email)
        rows = cursor.fetchall()
        # for row in rows:
        #     print("{0} {1} {2}".format(row[0], row[1], row[2]))
        return rows    
    elif operation == 'PUT':
        email = event['email']
        interest = event['interest']
        name = event['name']
        phone_number = event['phone_number']
        
        cursor = connection.cursor()
        query = "UPDATE USER SET interest = '{}', name = '{}', phone_number = '{}' WHERE email='{}'".format(interest, name, phone_number, email)
        print('query : ', query)
        cursor.execute(query)
        connection.commit()
        return "성공"



# def lambda_handler(event, context):
#     email = event['email']
#     interest = event['interest']
#     name = event['name']
#     phone_number = event['phone_number']
    
#     cursor = connection.cursor()
#     query = "INSERT INTO USER VALUES ('{}','{}','{}','{}')".format(email, interest, name, phone_number)
#     print('query : ', query)
#     cursor.execute(query)
#     connection.commit()
#     return "성공"


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
