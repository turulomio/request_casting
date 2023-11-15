from request_casting import request_casting
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status

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
    print(a)
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
