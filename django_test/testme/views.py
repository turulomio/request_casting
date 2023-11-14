from request_casting import request_casting
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status

@api_view(['GET', 'POST'])    
def integer(request):
    a=request_casting.RequestInteger(request, "a")
    return Response({"a": a}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])    
def string(request):
    a=request_casting.RequestString(request, "a")
    return Response({"a": a}, status=status.HTTP_200_OK)
