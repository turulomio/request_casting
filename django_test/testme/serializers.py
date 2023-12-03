from rest_framework import serializers
from testme import models

class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Record
        fields = ('url', 'id', 'datetime', 'user')

class PostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Posts
        fields = ('url', 'id', 'datetime', 'user')

