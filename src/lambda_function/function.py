import boto3
import logging.config

client = boto3.client('ssm')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
	logger.debug('Event :{}'.format(event))
	if 'GetParameter' in event:
		return _get_parameters([event['GetParameter']['Name']])
	elif 'GetParameters' in event:
		return _get_parameters(event['GetParameters']['Names'])
	elif 'GetParametersByPath' in event:
		return _get_parameters_by_path(event['GetParametersByPath']['Path'], event['GetParametersByPath']['Recursive'])
	elif 'PutParameter' in event:
		return _put_parameter(event['PutParameter'])
	raise ValueError('Event does not contain expected parameters. Event: {}'.format(event)) 
	

def _get_parameters(names):
	response = client.get_parameters(
		Names=names,
		WithDecryption=True
	)
	return _transform_return_parameters(response.get('Parameters', []))


def _get_parameters_by_path(path, recursive):
	response = client.get_parameters_by_path(
		Path=path, 
		Recursive=recursive,
		WithDecryption=True
	)
	return _transform_return_parameters(response.get('Parameters', []))

def _transform_return_parameters(parameters):
	transformed_parameters = {}
	for parameter in parameters:
		name = parameter['Name']
		value = parameter['Value'] if parameter['Type'] != 'StringList' else parameter['Value'].split(',')
		if name.startswith('/'):
			name_elements = name[1:].split('/')
			node = _make_or_traverse_path(transformed_parameters, name_elements[:-1])
			if not isinstance(node, dict):
				raise ValueError('Parameter {} is both a node and a leaf. This is not supported.'.format('/'.join(name_elements[:-1])))
			node[name_elements[-1:][0]] = value
		else:
			transformed_parameters[name] = value
	return transformed_parameters


def _make_or_traverse_path(parameters, elements):
	if not elements:
		return parameters
	if elements[0] not in parameters:
		parameters[elements[0]] = {}
	return _make_or_traverse_path(parameters[elements[0]], elements[1:])


def _put_parameter(parameter):
	if isinstance(parameter['Value'], (list, tuple)):
		if parameter.get('Secure', False):
			raise ValueError('Cannot have secure StringList')
		parameter_type = 'StringList'
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
