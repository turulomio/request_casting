from datetime import datetime,  date, timedelta
from zoneinfo import ZoneInfo
from decimal import Decimal

class RequestCastingError(Exception):
    pass

## Converts strings True or False to boolean
## @param s String
## @return Boolean
def string2bool(value):
    if value=="0" or value.lower()=="false":
        return False
    elif value=="1" or value.lower()=="true":
        return True
    else:
        raise RequestCastingError(f"Error in string2bool with value {value} with class {value.__class__}")

def string2date(value):
    """
        @param value Must be a string with iso format "2023-11-18"
    """
    try:
            d=value.split("-")
            return date(int(d[0]), int(d[1]),  int(d[2]))
    except:
        raise RequestCastingError(f"Error in string2date with value {value} with class {value.__class__}")


def string2dtaware(s, timezone_string=None):
    """
        @param s is a datetime isostring UTC Zone
        @param timezone_string If None returns a datetime aware in UTC zoneinfo, else a datetime aware y timezone_string zoneinfo
    """
    s=s.replace("T"," ").replace("Z","")
    
    #Gets naive datetime
    arrPunto=s.split(".")
    s=arrPunto[0]
    micro=int(arrPunto[1]) if len(arrPunto)==2 else 0
    dt_naive=datetime.strptime( s, "%Y-%m-%d %H:%M:%S" )
    dt_naive=dt_naive+timedelta(microseconds=micro)
    
    # Gets aware datetime  
    dt_aware=dt_naive.replace(tzinfo=ZoneInfo("UTC"))
#    print(dt_naive, dt_aware, dt_aware.astimezone(ZoneInfo("Europe/Madrid")))
    if timezone_string is None:
        return dt_aware
    else:
        return dt_aware.astimezone(ZoneInfo(timezone_string))

## Returns a model object
def RequestUrl(request, field, class_,  default=None, select_related=[], prefetch_related=[], model_url=None):   
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default
    return  object_from_url(dictionary.get(field), class_, model_url, select_related, prefetch_related)

## Returns a query_set obect
def RequestListOfUrls(request, field, model_class,   default=None,select_related=[],prefetch_related=[], model_url=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
    if not field in dictionary:
        return default

    r=queryset_from_list_of_urls(dictionary.getlist(field), model_class, model_url, select_related, prefetch_related)
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
        return  string2bool(dictionary.get(field))
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
            r.append(string2bool(i))
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
        return string2dtaware(dictionary.get(field), timezone_string)
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
    try:
        parts=url.split("/")
        return int(parts[len(parts)-2])
    except:
        raise RequestCastingError(f"I couldn't get id from this url: {url}")

def parse_from_url(url, model_class, model_url=None):
    """
        By default this method validates that url has the name of the class_ in lowercase as model_url
        For example. Products model should contain /products/ in url and then its id
                     ProductsMine should contain /productsmain/ or /products_main/ or /products-main/
        If your url is not in the ones before, you can use model_url to pass your own url to validate
        If we woudn't validate a param could pass other model with the same id and give wrong results
        
        Parameters:
            - class_: Class of the model we want to get. For example. models.Record
            - model_url -> str: String with the string before the id, without the slashes http://localhost/api/records/1/ -> records
            
        You don't need to pass model_url if models.__class__name.lower.replace("_").replace("-") == string before the id
        Returns a tuple (class_model, and id) from a django hyperlinked url
        For example https://localhost/api/products/1/ ==> (models.Products, 1)
    """
    def exception():
        raise RequestCastingError(f"Url ({url}) couldn't be parsed. Model: {model_class.__name__}. Real string before id: {model_url}")
    #########################################
    if url is None:
        exception()
    
    if model_url is None:
        model_url=model_class.__name__.lower().replace("-","").replace("_","") 

    try:
        parts=url.split("/")
        url_string_before_id=parts[len(parts)-3].lower().replace("-","").replace("_","")
        url_id= int(parts[len(parts)-2])
    except:
        exception()

    if url_string_before_id == model_url :
        return (model_class, url_id)
    else:
        exception()

def object_from_url(url, model_class, model_url=None,  select_related=[], prefetch_related=[]):
    """
        No exceptions and validations needed due to everything is tested in parse_from_url
    """
    model, id=parse_from_url(url, model_class, model_url )
    return model_class.objects.prefetch_related(*prefetch_related).select_related(*select_related).get(pk=id)

def queryset_from_list_of_urls(list_, model_class, model_url=None,  select_related=[], prefetch_related=[]):
    ids=[]
    for url in list_:
        model, id=parse_from_url(url, model_class, model_url)
        ids.append(id)
    return model_class.objects.filter(pk__in=ids).prefetch_related(*prefetch_related).select_related(*select_related)

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
