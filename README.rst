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
- AWS Parameter Store  :GetParameter
- AWS Parameter Store  :GetParameters
- AWS Parameter Store  :GetParameterByPath
- AWS Parameter Store  :PutParameter

Environment Variables
---------------------
**SSM_KMS_KEY_ARN** (Optional)
   The arn of the KMS key used for encryption and decryption of SecureString parameters.

Request Syntax
---------------------
The event is passed in as a JSON object. For example,

{
  "GetParameters": {
    "Names": [] - this will always be an array, for one parameter it will simply be an array of one
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
For GetParameter :

"Parameters": {
      "name": { - the name of the parameter is the key
          "Type": "String" | "StringList" | "SecureString",
          "Value': 'string' | ['string'], - the [] is if it was a StringList
          "Version": 123,
          "Selector": "string",
          "SourceResult": "string",
          "LastModifiedDate": "datetime",
          "ARN": "string"
      },
}

For PutParameter:
 "Version": 123

License: `APL2`_