import boto3
import logging.config

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
				response = get_parameter_from_store(body['Name'])
			elif 'Names' in body:
				response = get_parameter_from_store(body['Names'])
			else:
				logger.info('Missing the parameter name in the event')
		elif action == 'PutParameter':
				response = put_parameter_to_store(body['Name'], body['Type'], body['Value'])
            					
    else:
		logger.info('Missing action (get/put) in event body')	
	return response
	
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
		return response['Parameter']['Value']
		
		
def put_parameter_to_store(name, type_of_parameter, value):
	if type_of_parameter == "SecureString":
		response = client.put_parameter(KeyId=kms_key, Name=name, Type=type, Value=value)
    elif type_of_parameter == "String":
		response = client.put_parameter(Name=name, Type=type, Value=value)
	return response
