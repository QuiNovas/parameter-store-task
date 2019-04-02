============================
parameter-store-task
============================

.. _APL2: http://www.apache.org/licenses/LICENSE-2.0.txt

This lambda function is designed to get and put parameters from AWS Parameter Store for AWS Step Functions. The step functions will invoke the lambda based on the input event and state machine definition. 
This function should allow for

#. Getting a parameter, multiple parameters or parameters by path
#. Putting a single parameter or multiple parameters

Required AWS Resources
----------------------
AWS Parameter Store 

Required Permissions
--------------------
- ssm:GetParameter
- ssm:GetParameters
- ssm:GetParametersByPath
- ssm:PutParameter

Request Syntax
---------------------
The event is passed in as a JSON object. For example,

.. code-block:: JSON

  {
    "GetParameter": {
      "Name": "name"
    },
    "GetParameters": {
      "Names": ["name1", "name2]
    },
    "GetParametersByPath": {
      "Path": "" - required,
      "Recursive": true | false - required
    },
    "PutParameter": {
      "Name": "", - required
      "Description": "", - optional
      "Value": "" | [], - required. If a list, will be converted to a StringList
      "Secure": true | false, - defaults to false. Throws error if true and "Value" is a []
      "KeyId": "",  - optional
      "Overwrite": true|false, - optional, default is false
    }
  }

Response Syntax
---------------------
For GetParameter, GetParameters and GetParametersByPath :

.. code-block:: JSON

  {
    "name": "value" | ["value1", "value2"],
  }

For PutParameter:

.. code-block:: text

  123

License: `APL2`_
