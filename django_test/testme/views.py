from request_casting import request_casting
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status, viewsets
from testme import models, serializers

class RecordViewSet(viewsets.ModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer

@api_view(['GET', 'POST'])    
def integer(request):
    a=request_casting.RequestInteger(request, "a")
    return Response({"a": a, "class": a.__class__.__name__}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])    
def string(request):
    a=request_casting.RequestString(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])    
def bool(request):
    a=request_casting.RequestBool(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])    
def date(request):
    a=request_casting.RequestDate(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])    
def decimal(request):
    a=request_casting.RequestDecimal(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])    
def dtaware(request):
    a=request_casting.RequestDtaware(request, "a", "UTC")
    return Response({"a": a,  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])    
def list_of_bools(request):
    if request.method=="GET":
        a=request_casting.RequestListOfBools(request, "a[]")
    else:
        a=request_casting.RequestListOfBools(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])    
def list_of_integers(request):
    if request.method=="GET":
        a=request_casting.RequestListOfIntegers(request, "a[]")
    else:
        a=request_casting.RequestListOfIntegers(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])    
def list_of_strings(request):
    if request.method=="GET":
        a=request_casting.RequestListOfStrings(request, "a[]")
    else:
        a=request_casting.RequestListOfStrings(request, "a")
    return Response({"a": a,  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)     
    
@api_view(['GET', 'POST'])    
def list_of_urls(request):
    if request.method=="GET":
        a=request_casting.RequestListOfUrls(request, "a[]", models.Record)
    else:
        a=request_casting.RequestListOfUrls(request, "a", models.Record)
    return Response({"a": None if a is None else len(a),  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)     
    
@api_view(['GET', 'POST'])    
def url(request):
    a=request_casting.RequestUrl(request, "a", models.Record)
    return Response({"a": str(a),  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)     
    

    
