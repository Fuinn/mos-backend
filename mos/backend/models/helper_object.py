from django.db import models
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.postgres.fields import JSONField

class HelperObject(models.Model):

    # Type choices
    TYPE_PRE = 'pre'
    TYPE_POST = 'post'
    TYPE_CHOICES = [
        (TYPE_PRE, 'Pre-optimization'),
        (TYPE_POST, 'Post-optimization')
    ]

    name = models.CharField(max_length=100)

    description = models.TextField(default='No description')

    type = models.CharField(choices=TYPE_CHOICES,
                            max_length=100)

    data = JSONField(blank=True, null=True)
    data_size = models.IntegerField(default=0)

    model = models.ForeignKey('Model',
                              related_name='helper_objects',
                            on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='helper_objects',
                              on_delete=models.CASCADE)

class HelperObjectSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='helper-object-detail')

    data = serializers.SerializerMethodField()

    model = serializers.HyperlinkedRelatedField(view_name='model-detail',
                                                read_only=True,
                                                many=False)

    def get_data(self, obj):

        if obj.data is not None:
            return '{}data'.format(reverse('helper-object-detail', 
                                           args=[obj.id],
                                           request=self.context['request']))
        else:
            return None

    class Meta:
        model = HelperObject
        fields = ('url',
                  'id',
                  'name',
                  'description',
                  'type',
                  'data',
                  'data_size',
                  'model',)
