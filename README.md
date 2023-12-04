# request_casting
Python module that allows to cast django request data for POST and GET methods easyly

Allows you to capture errors in parameters and give them default values, to protect your application with little code and easy to read.


## Installation
You can use pip to install this module
```bash
pip install request_casting
```

## Casts

### RequestBool
Gets a parameter from a djangorestframework or django view and cast it to a bool object. For example

```python  
from request_casting import request_casting
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['GET', 'POST'])    
def myview(request):
    a=request_casting.RequestBool(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__}, status=status.HTTP_200_OK)
```

You can call this view with a GET method with requests, curl, axios...

```bash
curl http://localhost:8000/myview/?a=true
curl -X POST http://localhost:8000/myview/ -d"a=false"
```

You'll get this answer in both cases

```
{"a":true,"class":"bool"}
```

All request_casting methods allow to set a default value. By default this value is None in all Request methods.  This value is returned when cast fails.

```bash
curl http://localhost:8000/myview/?a=BADBOOL
```

You'll get this answer in both cases

```
{"a":null,"class":"NoneType"}
```



### RequestDate
Use this method inside a view to get a casted date. Use dates in Iso format

```python
    # ... The same as RequestBool example
    a=request_casting.RequestDate(request, "a")
```
You'll get this answers
``` 
curl http://localhost:8000/myview/?a=BADDATE   => a will be None
curl http://localhost:8000/myview/?a=2021-1-1   => a will be date(2023,1,1)
```

### RequestDecimal

Use this method inside a view to get a casted Decimal

```python
    # ... The same as RequestBool example
    a=request_casting.RequestDecimal(request, "a", Decimal(0))
```
You'll get this answers
``` 
curl http://localhost:8000/myview/?a=12.1212  => a will be Decimal(12.1212)
curl http://localhost:8000/myview/?a=2021-1-1   => a will be Decimal(0)
```

### RequestDtaware
Use this method inside a view to get a datetime with timezone. Use dates in Iso format

```python
    # ... The same as RequestBool example
    a=request_casting.RequestDtaware(request, "a")
```
You'll get this answers
``` 
curl http://localhost:8000/myview/?a=2011-10-05T14:48:00.000Z   => a will be a datetime with timezone
curl http://localhost:8000/myview/?a=2021-1-1   => a will be None
```

### RequestInteger

Use this method inside a view to get a casted Integer

```python
    # ... The same as RequestBool example
    a=request_casting.RequestInteger(request, "a")
```
You'll get this answers
``` 
curl http://localhost:8000/myview/?a=12 => a will be 12
curl http://localhost:8000/myview/?a=BADINTEGER  => a will be None
```


### RequestListOfBools

Use this method inside a view to get a list of Booleans

```python
    # ... The same as RequestBool example
    a=request_casting.RequesListOfBools(request, "a")
```
You'll get this answers
``` bash
curl "http://localhost:8000/myview/?a[]=true&a[]=false"   => a will be a list [True,False]
```

### RequestListOfIntegers


Use this method inside a view to get a list of Integers

```python
    # ... The same as RequestBool example
    a=request_casting.RequestListOfIntegers(request, "a")
```
You'll get this answers
``` bash
curl "http://localhost:8000/myview/?a[]=1&a[]=2"   => a will be a list [1,2]
```

### RequestListOfStrings


Use this method inside a view to get a list of strings

```python
    # ... The same as RequestBool example
    a=request_casting.RequestListOfStrings(request, "a")
```
You'll get this answers
``` bash
curl "http://localhost:8000/myview/?a[]=a&a[]=b"   => a will be a list ["a","b"]
```


### RequestString

Use this method inside a view to get a casted String

```python
    # ... The same as RequestBool example
    a=request_casting.RequestString(request, "a")
```
You'll get this answers
``` 
curl http://localhost:8000/myview/?a=12 => a will be "12"
curl http://localhost:8000/myview/?a=BADINTEGER  => a will be "BADINTEGER"
```


### RequestUrl

Use this method inside a view to get a django model object using its hyperlinked url

```python
    # ... The same as RequestBool example
    a=request_casting.RequestUrl(request, "a", models.Record, model_url="records")
```
You'll get this answers
``` bash
curl "http://localhost:8000/myview/?a=http://localhost:8000/api/records/1/"   => a will be a Record object with pk=1
```

### RequestListOfUrls


Use this method inside a view to get a list of django model object using its hyperlinked url

```python
    # ... The same as RequestBool example
    a=request_casting.RequestListOfUrls(request, "a",models.Record, model_url="records")
```
You'll get this answers
``` bash
curl "http://localhost:8000/myview/?a[]=http://localhost:8000/api/records/1/&a[]=http://localhost:8000/api/records/2/"   => a will be a list with Record objects with pk=1 and pk=2
```


## Other usefull functions

### all_args_are_not_empty

Returns True if all function arguments are different to None and ""

It's very usefull to compare view parameters fast.

```python
    request_casting.all_args_are_not_empty(None, "", None) #Returns False
    request_casting.all_args_are_not_empty("", "", "")# Returns False
    request_casting.all_args_are_not_empty(1, 1, 1) #Return True
```

### all_args_are_not_none


Returns True if all function arguments are different to None 

It's very usefull to compare view parameters fast.

```python
    request_casting.all_args_are_not_none(None, "", None) #Returns False
    request_casting.all_args_are_not_none("", "", "")# Returns True
    request_casting.all_args_are_not_none(1, 1, 1) #Return True
```

## Test module

Run `poe coverage` to test module.

## Changelog

### 0.3.0 (2023-12-04)
- Improved parse_from_url and object_from_url validations
- Added validate_object to RequestUrl and RequestListOfUrls to validate returned objects
- Added gettext support

### 0.2.0 (2023-11-18)
- Improving documentation
- All default values are set to None, including RequestList methods
- string2dtaware now uses ZoneInfo instead of pytz

### 0.1.0 (2023-11-15)
- Converted reusingcode module to an independent module
