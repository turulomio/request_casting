from decimal import Decimal
from gettext import translation
from importlib.resources import files
from pydicts import casts
        
try:
    t=translation('request_casting', files("request_casting") / 'locale')
    _=t.gettext
except:
    _=str


class RequestCastingError(Exception):
    pass


def RequestUrl(request, field, class_,  default=None, select_related=[], prefetch_related=[], model_url=None, validate_object=None):   
    """
        Returns an object of the model in class_ after parse url and validate with model_url
        
        Returns default if Can't be got
        
        Parameters:
            - validate_object: callable (function or lambda) that returns a boolean to validate got object. For example if object belongs to request.user
        
    """
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default
    
    try:
        o=object_from_url(dictionary.get(field), class_, model_url, select_related, prefetch_related)
    except:
        return None
        
    if validate_object is not None and o is not None and validate_object(o)==True:
        return o
    else:
        return None

## Returns a query_set obect
def RequestListOfUrls(request, field, model_class,   default=None,select_related=[],prefetch_related=[], model_url=None, validate_object=None):
    """
        This method try to parse get or post parameters. So is not for get a big amount of urls. So This method will no use querysets
        
        It will use RequestUrl. If some object can't be obtained, It will give None in its position        
        
        Parameters:
            - validate_object: callable (function or lambda) that returns a boolean to validate got object. For example if object belongs to request.user    
    """
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
    if not field in dictionary:
        return default
    r=[]
    for url in  dictionary.getlist(field):
        r.append(RequestUrl(request, field, model_class, default, select_related, prefetch_related, model_url, validate_object))
    return r

def RequestDate(request, field, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default
    try:
        return casts.str2date(dictionary.get(field))
    except:
        raise RequestCastingError(_("Error in RequestDate with method {0}").format(request.method))

def RequestBool(request, field, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default
    try:
        return  casts.str2bool(dictionary.get(field))
    except:
        raise RequestCastingError(_("Error in RequestBool with method {0}").format(request.method))

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
        raise RequestCastingError(_("Error in RequestDecimal with method {0}").format(request.method))

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
        raise RequestCastingError(_("Error in RequestInteger with method {0}").format(request.method))

def RequestListOfStrings(request, field, default=None):    
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        r=[]
        if dictionary.__class__==dict:
            for value in dictionary[field]:
                r.append(str(value))
        else:#Querydict
            items=dictionary.getlist(field, [])
            for i in items:
                r.append(str(i))
        return r
    except:
        raise RequestCastingError(_("Error in RequestListOfStrings with method {0}").format(request.method))

def RequestListOfBools(request, field, default=None):    
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        r=[]
        if dictionary.__class__==dict:
            for value in dictionary[field]:
                r.append(bool(value))
        else:#Querydict
            items=dictionary.getlist(field, [])
            for i in items:
                r.append(casts.str2bool(i))
        return r
    except:
        raise RequestCastingError(_("Error in RequestListOfBools with method {0}").format(request.method))
        
def RequestListOfIntegers(request, field, default=None,  separator=","):
    """
        If format=json in client post returns a dictionary instead of a querydict
        
        dictionary hasn't querydict.getlist method
    """
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        r=[]
        if dictionary.__class__==dict:
            for value in dictionary[field]:
                r.append(int(value))
        else:#Querydict
            items=dictionary.getlist(field, [])
            for i in items:
                r.append(int(i))
        return r
    except:
        raise RequestCastingError(_("Error in RequestListOfIntegers with method {0}").format(request.method))

def RequestDtaware(request, field, timezone_string, default=None):
    if request.method=="GET":
        dictionary=request.GET
    else:
        dictionary=request.data
        
    if not field in dictionary:
        return default

    try:
        return casts.str2dtaware(dictionary.get(field), "JsUtcIso",  timezone_string)
    except:
        raise RequestCastingError(_("Error in RequestDtaware with method {0}").format(request.method))



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
        raise RequestCastingError(_("Error in RequestString with method {0}").format(request.method))



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
        raise RequestCastingError(_("I couldn't get id from this url: {0}").format(url))

def parse_from_url(url, model_class, model_url=None):
    """
        If we woudn't validate a param could pass other model with the same id and give wrong results
        
        Parameters:
            - class_: Class of the model we want to get. For example. models.Record
            - model_url -> str: String with the string before the id, without the slashes http://localhost/api/records/1/ -> records
            
        You don't need to pass model_url if models.__class__name.lower.replace("_").replace("-") == string before the id
        Returns a tuple (class_model, and id) from a django hyperlinked url
        For example https://localhost/api/products/1/ ==> (models.Products, 1)
    """
    def exception():
        raise RequestCastingError(_("Url ({0}) couldn't be parsed. Model: {1}. Real string before id: {2}").format(url, model_class.__name__, model_url))
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
