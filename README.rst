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
The event is passed in as a JSON object. For example, to get a parameter from AWS parameter store, the request JSON is as follows

{   
  
  "Body" :
    {
      
      "Action":"GetParameter",
      "Name": "string",
      "WithDecryption": boolean
   
    }

}

Response Syntax
---------------------
{
      "Name":"string",
      "Value":"string"

}

License: `APL2`_