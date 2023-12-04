from request_casting import request_casting
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status, viewsets
from testme import models, serializers
from django.contrib.auth.models import User

class RecordViewSet(viewsets.ModelViewSet):
    queryset = models.Record.objects.all()
    serializer_class = serializers.RecordSerializer

class PostsViewSet(viewsets.ModelViewSet):
    queryset = models.Posts.objects.all()
    serializer_class = serializers.PostsSerializer

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
        a=request_casting.RequestListOfUrls(request, "a[]", models.Record, model_url="records")
    else:
        a=request_casting.RequestListOfUrls(request, "a", models.Record, model_url="records")
    return Response({"a": None if a is None else len(a),  "class": a.__class__.__name__ }, status=status.HTTP_200_OK)     
    
@api_view(['GET', 'POST'])
def url(request):
    a=request_casting.RequestUrl(request, "a", models.Record, model_url="records", validate_object=lambda o: o.user==User.objects.get(pk=1))
    return Response({"a": str(a),  "class": a.__class__.__name__}, status=status.HTTP_200_OK)     
    

    
