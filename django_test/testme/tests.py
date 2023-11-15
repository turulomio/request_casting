from datetime import datetime, date
from decimal import Decimal
from django.utils import timezone
from request_casting import request_casting
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from testme import models

class CtTestCase(APITestCase):    
    

    @classmethod
    def setUpClass(cls):
        """
            Only instantiated once
        """
        super().setUpClass()
        
        cls.user1 = User(
            email='user1@testing.com',
            first_name='User1',
            last_name='User1',
            username='user1',
        )
        cls.user1.set_password('user1')
        cls.user1.save()        
        
        cls.user2 = User(
            email='user2@testing.com',
            first_name='User2',
            last_name='User2',
            username='user2',
        )
        cls.user2.set_password('user2')
        cls.user2.save()
        
        # User to confront security
        cls.user_authorized_2 = User(
            email='other@other.com',
            first_name='Other',
            last_name='Other',
            username='other',
        )
        cls.user_authorized_2.set_password('other123')
        cls.user_authorized_2.save()

        for i in range(5):
            record=models.Record()
            record.datetime=timezone.now()
            record.user=cls.user1
            record.save()
            
            record=models.Record()
            record.datetime=timezone.now()
            record.user=cls.user2
            record.save()

        print(models.Record.objects.all())
    
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
        
        
        
    def test_get_decimal(self):
        client = APIClient()
        
        r=client.get("/decimal/?a=2023.12")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], 2023.12)
        self.assertEqual(r.json()["class"], "Decimal")
    
        r=client.post("/decimal/",  {"a": Decimal(12.123) })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], 12.123)
        self.assertEqual(r.json()["class"], "Decimal")
        
        with self.assertRaises(request_casting.RequestCastingError):
            r=client.get("/decimal/?a=baddecimal")        

    def test_get_dtaware(self):
        client = APIClient()
        
        r=client.get("/dtaware/?a=2011-10-05T14:48:00.000Z")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], "2011-10-05T14:48:00Z")
        self.assertEqual(r.json()["class"], "datetime")
    
        r=client.post("/dtaware/",  {"a": datetime.utcnow() })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["class"], "datetime")
        
        with self.assertRaises(request_casting.RequestCastingError):
            r=client.get("/dtaware/?a=baddt")

    def test_get_list_of_bools(self):
        client = APIClient()
        
        r=client.get("/list/bools/?a[]=true&a[]=false")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], [True, False])
        self.assertEqual(r.json()["class"], "list")
    
        r=client.post("/list/bools/", {"a":[True,False], })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], [True, False])
        self.assertEqual(r.json()["class"], "list")
        
    def test_get_list_of_strings(self):
        client = APIClient()
        
        r=client.get("/list/strings/?a[]=Elvis&a[]=Presley")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], ["Elvis", "Presley"])
        self.assertEqual(r.json()["class"], "list")
    
        r=client.post("/list/strings/", {"a":["Elvis", "Presley"], })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], ["Elvis",  "Presley"])
        self.assertEqual(r.json()["class"], "list")
