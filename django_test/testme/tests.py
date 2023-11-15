from datetime import date
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

class CtTestCase(APITestCase):    
    def test_get_integer(self):
        client = APIClient()
        
        r=client.get("/integer/?a=1")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], 1)
        self.assertEqual(r.json()["class"], "int")
    
        r=client.post("/integer/",  {"a":1, })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], 1)
        self.assertEqual(r.json()["class"], "int")
        
    def test_get_string(self):
        client = APIClient()
        
        r=client.get("/string/?a=hi")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], "hi")
        self.assertEqual(r.json()["class"], "str")
    
        r=client.post("/string/",  {"a":"hi", })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], "hi")
        self.assertEqual(r.json()["class"], "str")
        
    def test_get_bool(self):
        client = APIClient()
        
        r=client.get("/bool/?a=true")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], True)
        self.assertEqual(r.json()["class"], "bool")
    
        r=client.post("/bool/",  {"a": True, })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], True)
        self.assertEqual(r.json()["class"], "bool")
        
    def test_get_date(self):
        client = APIClient()
        
        r=client.get("/date/?a=2023-1-1")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], "2023-01-01")
        self.assertEqual(r.json()["class"], "date")
    
        r=client.post("/date/",  {"a":date(2023, 1, 1), })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], "2023-01-01")
        self.assertEqual(r.json()["class"], "date")
        
