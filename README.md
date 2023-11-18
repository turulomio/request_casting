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

All request_casting methods allow to set a default value. By default this value is None or an empty list in RequestList methods.  This value is returned when cast fails.

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
    a=request_casting.RequesDate(request, "a")
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
    a=request_casting.RequesDecimal(request, "a", Decimal(0))
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
    a=request_casting.RequesDtaware(request, "a")
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
    a=request_casting.RequetInteger(request, "a")
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
    a=request_casting.RequesListOfIntegers(request, "a")
```
You'll get this answers
``` bash
curl "http://localhost:8000/myview/?a[]=1&a[]=2"   => a will be a list [1,2]
```

### RequestListOfStrings

### RequestString

### RequestUrl

### RequestListOfUrls

## Other usefull functions

### all_args_are_not_empty

### all_args_are_not_none

## Test module

poe coverage

## Changelog

### 0.1.0 (2023-11-15)
- Converted reusingcode module to an independent module
