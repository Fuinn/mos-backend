from django.db import models
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.postgres.fields import JSONField

class InterfaceObject(models.Model):

    # Type choices
    TYPE_INPUT = 'input'
    TYPE_OUTPUT = 'output'
    TYPE_CHOICES = [
        (TYPE_INPUT, 'Input'),
        (TYPE_OUTPUT, 'Output')
    ]

    name = models.CharField(max_length=100)

    description = models.TextField(default='No description', blank=True)

    type = models.CharField(choices=TYPE_CHOICES,
                            max_length=100)

    data = JSONField(blank=True, null=True)
    data_size = models.IntegerField(default=0)

    model = models.ForeignKey('Model',
                              related_name='interface_objects',
                              on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='interface_objects',
                              on_delete=models.CASCADE)

class InterfaceObjectSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='interface-object-detail')

    data = serializers.SerializerMethodField()

    model = serializers.HyperlinkedRelatedField(view_name='model-detail',
                                                read_only=True,
                                                many=False)

    def get_data(self, obj):
        
        if obj.data is not None:
            return '{}data'.format(reverse('interface-object-detail',
                                           args=[obj.id],
                                           request=self.context['request']))
        else:
            return None

    class Meta:
        model = InterfaceObject
        fields = ('url',
                  'id',
                  'name',
                  'description',
                  'type',
                  'data',
                  'data_size',
                  'model',)
