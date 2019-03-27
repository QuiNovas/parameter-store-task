import boto3
import json	
import logging.config
import os

kms_key = os.environ['SSM_KMS_KEY_ARN']
client = boto3.client('ssm')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
	logger.info('Event :{}'.format(event))
	body = event['Body']
	if 'Action' in body:
		action = body['Action']
		if action == 'GetParameter':
			if 'Name' in body:
				return get_parameter_from_store(body['Name'])
			elif 'Names' in body:
				return get_parameter_from_store(body['Names'])
			else:
				logger.info('Missing the parameter name in the event')
		elif action == 'PutParameter':
			return put_parameter_to_store(body['Name'], body['Type'], body['Value'])
		else:
			logger.info('Undefined action. Cannot complete the request')            					
	else:
		logger.info('Missing action (get/put) in event body')	

		
def get_parameter_from_store(name):
	if isinstance(name, list):
		parameter_list = []
		for each_name in name:
			params = {}
			response = client.get_parameter(Name=each_name, WithDecryption=True)
			params['Name'] = each_name
			params['Value'] = response['Parameter']['Value']
			parameter_list.append(params)
		return parameter_list
	else:
		response = client.get_parameter(Name=name, WithDecryption=True)
		return 'Value:{}'.format(response['Parameter']['Value'])
		

		
def put_parameter_to_store(name, type_of_parameter, value):
	if type_of_parameter == "SecureString":
		response = client.put_parameter(KeyId=kms_key, Name=name, Type=type_of_parameter, Value=value)
		return response['Version']
	elif type_of_parameter == "String":
		response = client.put_parameter(Name=name, Type=type_of_parameter, Value=value)
		return 'Version:{}'.format(response['Version'])
	else:
		logger.info('Unexpected type. Cannot put the parameter in store')
		
	#TODO for StringList
