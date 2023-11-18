from datetime import datetime,  date, timedelta, timezone
from decimal import Decimal

class RequestCastingError(Exception):
    pass

## Converts strings True or False to boolean
## @param s String
## @return Boolean
def str2bool(value):
    if value=="0" or value.lower()=="false":
        return False
    elif value=="1" or value.lower()=="true":
        return True
    else:
        raise RequestCastingError(f"Error in str2bool with value {value} with class {value.__class__}")


## Changes zoneinfo from a dtaware object
## For example:
## - datetime.datetime(2018, 5, 18, 8, 12, tzinfo=<DstTzInfo 'Europe/Madrid' CEST+2:00:00 DST>)
## - libcaloriestrackerfunctions.dtaware_changes_tz(a,"Europe/London")
## - datetime.datetime(2018, 5, 18, 7, 12, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
## @param dt datetime aware object
## @param tzname String with datetime zone. For example: "Europe/Madrid"
## @return datetime aware object
def dtaware_changes_tz(dt,  tzname):
    if dt==None:
        return None
    tzt=timezone(tzname)
    tarjet=tzt.normalize(dt.astimezone(tzt))
    return tarjet

def string2date(value):
    """
        @param value Must be a string with iso format "2023-11-18"
    """
    try:
            d=value.split("-")
            return date(int(d[0]), int(d[1]),  int(d[2]))
    except:
        raise RequestCastingError(f"Error in string2date with value {value} with class {value.__class__}")

def string2dtnaive(s, format):
    arrPunto=s.split(".")
    s=arrPunto[0]
    micro=int(arrPunto[1]) if len(arrPunto)==2 else 0
    dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S" )
    dt=dt+timedelta(microseconds=micro)
    return dt

def dtnaive2dtaware(dtnaive, tz_name):
    z=timezone(tz_name)
    return z.localize(dtnaive)

def string2dtaware(s, format, tz_name='UTC'):
        s=s.replace("T"," ").replace("Z","")
        dtnaive=string2dtnaive(s,"%Y-%m-%d %H:%M:%S.")
        dtaware_utc=dtnaive2dtaware(dtnaive, 'UTC')
        return dtaware_changes_tz(dtaware_utc, tz_name)

## Returns a model object
def RequestUrl(request, field, class_,  default=None, select_related=[], prefetch_related=[]):   
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default
    return  object_from_url(dictionary.get(field), class_, select_related, prefetch_related)

## Returns a query_set obect
def RequestListOfUrls(request, field, class_,  default=None,select_related=[],prefetch_related=[]):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
    if not field in dictionary:
        return default

    r=queryset_from_list_of_urls(dictionary.getlist(field), class_, select_related, prefetch_related)
    return r

def RequestDate(request, field, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default
    try:
        return string2date(dictionary.get(field))
    except:
        raise RequestCastingError(f"Error in RequestDate with method {request.method}")

def RequestBool(request, field, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default
    try:
        return  str2bool(dictionary.get(field))
    except:
        raise RequestCastingError(f"Error in RequestBool with method {request.method}")

def RequestDecimal(request, field, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        return Decimal(dictionary.get(field))
    except:
        raise RequestCastingError(f"Error in RequestDecimal with method {request.method}")

def RequestInteger(request, field, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data

    if not field in dictionary:
        return default

    try:
        return int(dictionary.get(field))
    except:
        raise RequestCastingError(f"Error in RequestInteger with method {request.method}")

def RequestListOfStrings(request, field, default=None):    
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        r=[]
        items=dictionary.getlist(field, [])
        for i in items:
            r.append(str(i))
        return r
    except:
        raise RequestCastingError(f"Error in RequestListOfStrings with method {request.method}")

def RequestListOfBools(request, field, default=None):    
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        r=[]
        items=dictionary.getlist(field)
        for i in items:
            r.append(str2bool(i))
        return r
    except:
        raise RequestCastingError(f"Error in RequestListOfBools with method {request.method}")
        
def RequestListOfIntegers(request, field, default=None,  separator=","):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        r=[]
        items=dictionary.getlist(field, [])
        for i in items:
            r.append(int(i))
        return r
    except:
        raise RequestCastingError(f"Error in RequestListOfIntegers with method {request.method}")

def RequestDtaware(request, field, timezone_string, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        return string2dtaware(dictionary.get(field), "JsUtcIso", timezone_string)
    except:
        raise RequestCastingError(f"Error in RequestDtaware with method {request.method}")


def RequestString(request, field, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default
    try:
        return dictionary.get(field)
    except:
        raise RequestCastingError(f"Error in RequestString with method {request.method}")


def ids_from_list_of_urls(list_):
    r=[]
    for url in list_:
        r.append(id_from_url(url))
    return r

def id_from_url(url):
    if url is None:
        return None
    parts=url.split("/")
    return int(parts[len(parts)-2])

def parse_from_url(url):
    """
        Returns a tuple (model_url and id) from a django hyperlinked url
        For example https://localhost/api/products/1/ ==> ('products', 1)
    """
    if url is None:
        return None,None
    try:
        parts=url.split("/")
        return parts[len(parts)-3], int(parts[len(parts)-2])
    except:
        print("Error parsing url", url)
        return None,None


def object_from_url(url, class_, select_related=[], prefetch_related=[], model_url=None):
    """
        By default this method validates that url has the name of the class_ in lowercase as model_url
        For example. Products model should contain /products/ in url and then its id
                     ProductsMine should contain /productsmain/ or /products_main/ or /products-main/
        If your url is not in the ones before, you can use model_url to pass your own url to validate
        If we woudn't validate a param could pass other model with the same id and give wrong results
    """
    if url is None:
        return None
    # Get id and model_url
    if model_url is None:
        model_url, id_=parse_from_url(url)
    else:
        id_=id_from_url(url)

    #Validation
    if id_ is None:
        return None

    if class_.__name__.lower() != model_url.lower().replace("-","").replace("_",""):
        comment=f"url couldn't be validated {url} ==> {class_.__name__} {model_url} {id_}"
        raise RequestCastingError(comment)

    #Get result
    return class_.objects.prefetch_related(*prefetch_related).select_related(*select_related).get(pk=id_from_url(url))

def queryset_from_list_of_urls(list_, class_, select_related=[], prefetch_related=[]):
    ids=ids_from_list_of_urls(list_)
    return class_.objects.filter(pk__in=ids).prefetch_related(*prefetch_related).select_related(*select_related)

## Returns false if some arg is None
def all_args_are_not_none(*args):
    for arg in args:
        if arg is None:
            return False
    return True

## Returns false if some args is None or ""
def all_args_are_not_empty(*args):
    for arg in args:
        if arg is None or arg=="":
            return False
    return True
