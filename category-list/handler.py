import boto3
import json

lambda_client = boto3.client('lambda', region_name='us-east-1')

def lambda_handler(event, context):
    lambda_response = lambda_client.invoke(
                    FunctionName = 'python-rds',
                    InvocationType = 'RequestResponse',
                    Payload = json.dumps(event)
                    )
    resp_str = lambda_response['Payload'].read()
    rds_response = json.loads(resp_str)
    # return rds_response
    if rds_response == 'no data':
        return rds_response
    
    ses = boto3.client('ses', region_name='us-east-1')
    
    for idx, res in enumerate(rds_response):
        try:
            body = f'{rds_response[idx][2]}, {rds_response[idx][4]}회차 {rds_response[idx][3]}시험일은 {rds_response[idx][5]}입니다.'
            
            ses_response = ses.send_email(
                Source='multicampusjmtgr@gmail.com',
                Destination={
                    'ToAddresses': [
                        # 'multicampusjmtgr@gmail.com',
                        # 'lys3d@naver.com',
                        rds_response[idx][0],
                    ]
                },
                Message={
                    'Subject': {
                        'Data': f'{rds_response[idx][2]} 자격증 시험정보 안내메일 입니다.',
                        'Charset': 'UTF-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': body,
                            'Charset': 'UTF-8'
                        }
                    }
                }
            )
        except:
            pass
    
    return rds_response