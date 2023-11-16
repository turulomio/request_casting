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
def bool(request):
    a=request_casting.RequestBool(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__}, status=status.HTTP_200_OK)
```

You can call this view with a GET method with requests, curl, axios...

```bash
curl http://localhost:8000/bool/?a=true
curl -X POST http://localhost:8000/bool/ -d"a=false"
```

You'll get this answer in both cases

```
{"a":true,"class":"bool"}
```


### RequestDate

### RequestDecimal

### RequestDtaware

### RequestInteger

### RequestListOfBools

### RequestListOfIntegers

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
