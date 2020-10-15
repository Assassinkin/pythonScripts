# lambda handler for the calc api endpoint with api-gateway taking care of the requests handling
import json
import math

def lambda_handler(event, context):
    if event['a'] == None or event['b'] == None or event['op'] == None:
        return {
            "statusCode": 400,
            "body": {
                'error': 'Invalid Input'
            }
        }
    res = dict()
    res['a'] = int(event['a'])
    res['b'] = int(event['b'])
    res['op'] = event['op']
    if math.isnan(res['a']) or math.isnan(res['b']):
        return {
            "statusCode": 400,
            "body": {
                'error': 'Invalid Operand'
            }
        }



    if event['op'] == '+' or event['op'] == 'add':
        res['c'] = res['a'] + res['b']
    elif event['op'] == '-' or event['op'] == 'sub':
        res['c'] = res['a'] - res['b']
    elif event['op'] == '*' or event['op'] == 'mul':
        res['c'] = res['a'] * res['b']
    elif event['op'] == '/' or event['op'] == 'div':
        if res['b'] == 0:
            res['c'] = None
        else: 
            res['c'] = res['a'] / res['b']
    else:
        return {
            "statusCode": 400,
            "body": {
                'error': 'Invalid Operator'
            }
        }
    return {
        "statusCode": 200,
        "body": res
    }