============================
parameter-store-task
============================

.. _APL2: http://www.apache.org/licenses/LICENSE-2.0.txt

This lambda function is designed to get and put parameters from AWS Parameter
Store for AWS Step Functions. The step functions will invoke the lambda based
on the input event and state machine definition.
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
The event is passed in as a JSON object. Examples:

.. code::

  {
    "GetParameter": {
      "Name": "string",
      "ResultFormat": "string"
    }
  }

  {
    "GetParameters": {
      "Names": ["string"],
      "ResultFormat": "string"
    }
  }

  {
    "GetParametersByPath": {
      "Path": "string",
      "Recursive": boolean,
      "RelativePath": boolean,
      "ResultFormat": "string"
    }
  }

  {
    "PutParameter": {
      "Name": "string",
      "Value": "string" | ["string"],
      "Description": "string",
      "Secure": booleran,
      "KeyId": "string",
      "Overwrite": boolean,
    }
  }

**GetParameter**
  :Name:
    The name of the parameter to get. REQUIRED
  :ResultFormat:
    The format of the result. ``VALUE_ONLY``, ``NAME_VALUE``,
    or ``NESTED_MAP``. OPTIONAL, defaults to ``NAME_VALUE``.

**GetParameters**
  :Names:
    The names of the parameter to get. REQUIRED
  :ResultFormat:
    The format of the result. ``NAME_VALUE``
    or ``NESTED_MAP``. OPTIONAL, defaults to ``NAME_VALUE``.

**GetParametersByPath**
  :Path:
    The path of the parameters to get. REQUIRED
  :Recursive:
    Whether to recurse through the parameter tree, starting
    at ``Path``. OPTIONAL - defaults to ``false``
  :RelativePath:
    If ``true``, will remove the path provided from the names returned.
    OPTIONAL, defaults to ``false``.
  :ResultFormat:
    The format of the result. ``NAME_VALUE``, ``NESTED_MAP``.
    OPTIONAL, defaults to ``NAME_VALUE``.

**PutParameter**
  :Name:
    The name of the parameter to put. REQUIRED
  :Value:
    The value of the parameter to put. If this is an `[]` then the type
    `StringList` will be used. REQUIRED
  :Description:
    The description of the parameter. OPTIONAL, defaults to empty
    string.
  :Secure:
    ``true`` if this parameter should be a ``SecureString``. OPTIONAL,
    defaults to ``false``.
  :KeyId:
    The AWS KMS Key Id to use to encrypt the parameter *if* ``Secure=true``.
    OPTIONAL, defaults to the account key for parameter encryption.
  :Overwrite:
    ``true`` if existing parameters should be overwritten. OPTIONAL,
    defaults to ``false``.

Result Formats
--------------
**VALUE_ONLY**
  Only the value of the parameter will be returned. For example:

  .. code::

    "MyValue"

**NAME_VALUE**
  The name and value of the parameter(s) will be returned in a flat map. For example:

  .. code::

    {
      "MyName": "MyValue",
      "path/to/MyName": "MyValue"
    }

**NESTED_MAP**
  The names of the parameters will be split by ``/``, with each sub-name becoming a map in
  the nested map returned. For example:

  .. code::

    {
      "MyName": "MyValue",
      "path": {
        "to": {
          "MyName": "MyValue"
        }
      }
    }

Behavior
--------
**GetParameter, GetParameters, GetParametersByPath**
  - If the parameter value is of type ``StringList`` then a ``["string"]`` will be returned.
**GetParameters, GetParametersByPath**
  - If the path contains a node that both has a value and has children and the ``ResultFormat`` is ``NESTED_MAP`` then a ValueError is raised.
**GetParametersByPath**
  - If ``RelativePath`` is set to ``true`` the the path removed will be up to and including the last occurance of ``/``.
**PutParameter**
  - If ``Value`` is a ``["string"]`` then a ``StringList`` will be created unless ``Secure`` is ``true``, in which case a ``SecureString`` will be created.


Response Syntax
---------------------
For GetParameter and GetParameters and
GetParametersByPath see Result Formats above.

For PutParameter, the version number is returned:

.. code::

  123

License: `APL2`_
