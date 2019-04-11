import boto3
import logging.config

client = boto3.client('ssm')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
	logger.debug('Event :{}'.format(event))
	if 'GetParameter' in event:
		return _get_parameter(event['GetParameter'])
	elif 'GetParameters' in event:
		return _get_parameters(event['GetParameters'])
	elif 'GetParametersByPath' in event:
		return _get_parameters_by_path(event['GetParametersByPath'])
	elif 'PutParameter' in event:
		return _put_parameter(event['PutParameter'])
	raise ValueError('Event does not contain expected parameters. Event: {}'.format(event)) 
	
def _get_parameter(arguments):
	response = client.get_parameter(
		Name=arguments['Name'],
		WithDecryption=True
	)
	result_format = arguments.get('ResultFormat', 'NAME_VALUE')
	if result_format == 'VALUE_ONLY':
		return _transform_value(response['Parameter']['Value'], response['Parameter']['Type'])
	elif result_format == 'NAME_VALUE':
		return _transform_parameter(response['Parameter'], result_format)
	else:
		raise ValueError('Unknown ResultFormat {} for GetParameter'.format(result_format))

def _get_parameters(arguments):
	response = client.get_parameters(
		Names=arguments['Names'],
		WithDecryption=True
	)
	result_format = arguments.get('ResultFormat', 'NAME_VALUE')
	if result_format == 'NAME_VALUE' or result_format == 'NESTED_MAP':
		result = {}
		for parameter in response['Parameters']:
			result = {**result, **_transform_parameter(parameter, result_format)}
		return result
	else:
		raise ValueError('Unknown ResultFormat {} for GetParameters'.format(result_format))

def _get_parameters_by_path(arguments):
	response = client.get_parameters_by_path(
		Path=arguments['Path'], 
		Recursive=arguments.get('Recursive', False),
		WithDecryption=True
	)
	result_format = arguments.get('ResultFormat', 'NAME_VALUE')
	if result_format == 'NAME_VALUE' or result_format == 'NESTED_MAP':
		result = {}
		for parameter in response['Parameters']:
			result = {**result, **_transform_parameter(parameter, result_format, '' if not arguments.get('RelativePath') else arguments['Path'])}
		return result
	else:
		raise ValueError('Unknown ResultFormat {} for GetParameters'.format(result_format))

def _transform_parameter(parameter, result_format, relative_path=''):
	name = parameter['Name'][relative_path.rfind('/')+1:]
	if result_format == 'NAME_VALUE':
		return {
			name: _transform_value(parameter['Value'], parameter['Type'])
		}
	elif result_format == 'NESTED_MAP':
		if parameter['Name'].startswith('/'):
			name_elements = parameter['Name'][1:].split('/')
			result = _make_path({}, name_elements[:-1])
			result[name_elements[-1:][0]] = _transform_value(parameter['Value'], parameter['Type'])
		else:
			result = {
				name: _transform_value(parameter['Value'], parameter['Type'])
			}
		return result

def _transform_value(value, value_type):
	if value_type == 'String' or value_type == 'SecureString':
		return value
	elif value_type == 'StringList':
		return value.split(',')
	else:
		raise ValueError('Unknown Type {}'.format(value_type))

def _make_path(parameters, elements):
	if not elements:
		return parameters
	parameters[elements[0]] = {}
	return _make_or_traverse_path(parameters[elements[0]], elements[1:])

def _put_parameter(parameter):
	if isinstance(parameter['Value'], (list, tuple)):
		parameter_type = 'SecureString' if parameter.get('Secure', False) else 'StringList'
		value = ','.join(parameter['Value'])
	else:
		parameter_type = 'SecureString' if parameter.get('Secure', False) else 'String'
		value = parameter['Value']
	if parameter_type == 'SecureString' and 'KeyId' in parameter:
		response = client.put_parameter(
			Name=parameter['Name'],
			Type=parameter_type,
			Value=str(value),
			KeyId=parameter['KeyId'],
			Description=parameter.get('Description', ''),
			Overwrite=parameter.get('Overwrite', False)
		)
	else:
		response = client.put_parameter(
			Name=parameter['Name'],
			Type=parameter_type,
			Value=str(value),
			Description=parameter.get('Description', ''),
			Overwrite=parameter.get('Overwrite', False)
		)
	return response['Version']
