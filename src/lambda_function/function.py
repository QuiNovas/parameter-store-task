import boto3
import json
import logging.config
import os

KMS_KEY = os.environ['SSM_KMS_KEY_ARN']
client = boto3.client('ssm')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
	logger.info('Event :{}'.format(event))
	if 'GetParameters' in event:
		response = _get_parameter_from_store(event['GetParameters']['Names'])
	elif 'GetParametersByPath' in event:
		response = _get_parameter_from_store_by_path(event['GetParametersByPath']['Path'], event['GetParametersByPath']['Recursive'])
	elif 'PutParameter' in event:
		response = _put_parameter_to_store(event['PutParameter'])
	else:
		return 'Unexpected request. Cannot be completed.'
	return response
	

def _get_parameter_from_store(names):
	parameters = {}
	parameters_list = {}
	for name in names:
		params = client.get_parameter(Name=name, WithDecryption=True)
		parameters[params['Parameter']['Name']] = params['Parameter']
		parameters_list["Parameters"] = parameters
	return json.dumps(parameters_list, indent=2, default=str)
	

def _get_parameter_from_store_by_path(path, recursive):
	parameters = {}
	response = {}
	parameters_list = []
	params = client.get_parameters_by_path(Path=path, Recursive=recursive)
	for i in range(0, len(params['Parameters'])):
		parameters[params['Parameters'][i]['Name']] = params['Parameters'][i]
		parameters_list.append(parameters)
	response["Parameters"] = parameters_list
	return json.dumps(response, indent=2, default=str)
	

def _put_parameter_to_store(put_param):
	if 'KeyId' in put_param:
		response = client.put_parameter(
								Name=put_param['Name'],
								Type=put_param['Type'],
								Value=put_param['Value'],
								KeyId=put_param['KeyId'],
								Description=put_param.get('Description', ''),
								Overwrite=put_param.get('Overwrite', False)
								)
	else:
		response = client.put_parameter(
										Name=put_param['Name'],
										Type=put_param['Type'],
										Value=(",".join(put_param['Value']))  if put_param['Type']=='StringList' else put_param['Value'],
										Description=put_param.get('Description', ''),
										Overwrite=put_param.get('Overwrite', False)
										)
	return 'Version:{}'.format(response['Version'])
								
								
								
	
		
		
		
		
		