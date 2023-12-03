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
            
            post=models.Posts()
            post.datetime=timezone.now()
            post.user=cls.user1
            post.save()
            
            post=models.Posts()
            post.datetime=timezone.now()
            post.user=cls.user2
            post.save()

#        print(models.Record.objects.all())
    
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
        
                
        with self.assertRaises(request_casting.RequestCastingError):
            r=client.get("/integer/?a=badinteger")        

        #To test default
        r=client.get("/integer/?not_a=12")
        
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
        
        #To test default
        r=client.get("/string/?not_a=12")
        
    def test_get_url(self):
        client = APIClient()
        r=client.get("/url/?a=http://localhost:8000/api/records/1/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        assert r.json()["a"].startswith("Record 1")
        self.assertEqual(r.json()["class"], "Record")
        
        r=client.post("/url/", {"a":"http://localhost:8000/api/records/1/"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        assert r.json()["a"].startswith("Record 1")
        self.assertEqual(r.json()["class"], "Record")
        
        with self.assertRaises(request_casting.RequestCastingError):
            r=client.post("/url/", {"a":"http://localhost:8000/api/notarecord/1/"})

        r=client.get("/url/?not_a=http://localhost:8000/api/records/1/")
        self.assertEqual(r.json()["a"], "None")

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
        
#        #To test RequestCastingError
#        r=client.get("/bool/?a=tyyui")
        
        #To test default
        r=client.get("/bool/?not_a=true")
        
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
        
#        with self.assertRaises(request_casting.RequestCastingError):
#            r=client.get("/date/?a=baddecimal")        
            
        #To test default
        r=client.get("/date/?not_a=2023-1-1")
            
        
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

        #To test default
        r=client.get("/decimal/?not_a=12.34")

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
        
        r=client.get("/list/strings/?not_a[]=Elvis&not_a[]=Presley")
        self.assertEqual(r.json()["a"], None)
        
    def test_get_list_of_integers(self):
        client = APIClient()
        
        r=client.get("/list/integers/?a[]=1&a[]=2")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], [1, 2])
        self.assertEqual(r.json()["class"], "list")
    
        r=client.post("/list/integers/", {"a":[1, 2,] })
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], [1, 2])
        self.assertEqual(r.json()["class"], "list")
        
        
    def test_get_list_of_urls(self):
        client = APIClient()
        r=client.get("/list/urls/?a[]=http://localhost:8000/api/records/1/&a[]=http://localhost:8000/api/records/3/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], 2)
        self.assertEqual(r.json()["class"], "QuerySet")
        
        r=client.post("/list/urls/", {"a": ["http://localhost:8000/api/records/1/", "http://localhost:8000/api/records/3/"]})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.json()["a"], 2)
        self.assertEqual(r.json()["class"], "QuerySet")
        
        r=client.get("/list/urls/?not_a[]=http://localhost:8000/api/record/1/&not_a[]=http://localhost:8000/api/record/2/")
        self.assertEqual(r.json()["a"], None)
        
    def test_all_args_are_not_none(self):
        r=request_casting.all_args_are_not_none(None, None, None)
        self.assertEqual(r, False)
        r=request_casting.all_args_are_not_none(None, 1, None)
        self.assertEqual(r, False)
        r=request_casting.all_args_are_not_none(1, 1, 1)
        self.assertEqual(r, True)
        r=request_casting.all_args_are_not_none("", "", "")
        self.assertEqual(r, True)

    def test_all_args_are_not_empty(self):
        r=request_casting.all_args_are_not_empty(None, "", None)
        self.assertEqual(r, False)
        r=request_casting.all_args_are_not_empty("", "", "")
        self.assertEqual(r, False)
        r=request_casting.all_args_are_not_empty(1, 1, 1)
        self.assertEqual(r, True)
        

    def test_parse_from_url(self):
        self.assertEqual(request_casting.parse_from_url("http://localhost:8000/api/records/1/", models.Record, "records"), (models.Record, 1))
        self.assertEqual(request_casting.parse_from_url("http://localhost:8000/api/records/100/", models.Record, "records"), (models.Record, 100))
        self.assertEqual(request_casting.parse_from_url("http://localhost:8000/api/posts/1/", models.Posts), (models.Posts, 1))
        self.assertEqual(request_casting.parse_from_url("http://localhost:8000/api/posts/1/", models.Posts, "posts"), (models.Posts, 1))
        
        with self.assertRaises(request_casting.RequestCastingError):
            request_casting.parse_from_url("http://localhost:8000/api/1/1/", models.Record)
        
        with self.assertRaises(request_casting.RequestCastingError):
            request_casting.parse_from_url("http://localhost:8000/api/records/rere/", models.Record)
            
    def test_object_from_url(self):
        self.assertEqual(request_casting.object_from_url("http://localhost:8000/api/records/1/", models.Record, "records").__class__, models.Record)
        self.assertEqual(request_casting.object_from_url("http://localhost:8000/api/records/1/", models.Record, "records").id, 1)
        with self.assertRaises(models.Posts.DoesNotExist):#No existe este id
            request_casting.object_from_url("http://localhost:8000/api/posts/100/", models.Posts)
        
 
