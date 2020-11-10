import json


def lambda_handler(event, context):
    try:
        params_arry = event['params']
        path_arry = params_arry['path']
        email = int(params_arry['email'])

        str_return = {'result' : 'TURE', 'email' : email}
    except Exception as e:
        str_return = {'result' : 'FALSE', 'error_type' : 'TypeError'}

    return str_return