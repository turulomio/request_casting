from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    user= models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'records'

    def __repr__(self):
        return f"Record {self.id} of user {self.user.username} took {self.datetime}"
        
    def __str__(self):
        return self.__repr__()

class Posts(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    user= models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'posts'

    def __repr__(self):
        return f"Post {self.id} of user {self.user.username} took {self.datetime}"
        
    def __str__(self):
        return self.__repr__()
