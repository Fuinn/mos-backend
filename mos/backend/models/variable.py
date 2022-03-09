from django.db import models
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class Variable(models.Model):

    # Types choices 
    TYPE_SCALAR = 'scalar'
    TYPE_ARRAY = 'array'
    TYPE_HASHMAP = 'hashmap'
    TYPE_UNKNOWN = 'unknown'
    TYPE_CHOICES = [
        (TYPE_SCALAR, 'Scalar'),
        (TYPE_ARRAY, 'Array'),
        (TYPE_HASHMAP, 'Hashmap'),
        (TYPE_UNKNOWN, 'Unknown')
    ] 

    name = models.CharField(max_length=100)
    description = models.TextField(default='No description')
    labels = models.CharField(max_length=100, default='', blank=True)
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_UNKNOWN, max_length=100)
    shape = JSONField(blank=True, null=True) # None for scalar/unknown
                                             # List of one element for hashmap
                                             # List of multiple elements for array
    
    model = models.ForeignKey('Model',
                              related_name='variables',
                              on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='variables',
                              on_delete=models.CASCADE)

class VariableState(models.Model):

    # Kind choices
    KIND_CONTINUOUS = 'continuous'
    KIND_INTEGER = 'integer'
    KIND_BINARY = 'binary'
    KIND_UNKNOWN = 'unknown'
    KIND_CHOICES = [
        (KIND_CONTINUOUS, 'Continuous'),
        (KIND_INTEGER, 'Integer'),
        (KIND_BINARY, 'Binary'),
        (KIND_UNKNOWN, 'Unknown')
    ]

    index = JSONField(blank=True, null=True)
    label = models.CharField(default="", blank=True, max_length=200)
    kind = models.CharField(choices=KIND_CHOICES, default=KIND_UNKNOWN, max_length=100)
    value = models.FloatField(default=0.)
    upper_bound = models.FloatField(default=0.)
    lower_bound = models.FloatField(default=0.)
    variable = models.ForeignKey('Variable',
                                 related_name='states',
                                 on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='variable_states',
                              on_delete=models.CASCADE)
    
class VariableSerializer(serializers.HyperlinkedModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(view_name='variable-detail')
    states = serializers.SerializerMethodField()
    model = serializers.HyperlinkedRelatedField(view_name='model-detail',
                                                read_only=True,
                                                many=False)

    def get_states(self, obj):

        return '{}?variable={}'.format(reverse('variable-state-list',
                                               request=self.context['request']),
                                        obj.id)

    class Meta:
        model = Variable
        fields = ('url',
                  'id',
                  'name',
                  'description',
                  'labels',
                  'type',
                  'shape',
                  'states',
                  'model',)
    
class VariableStateSerializer(serializers.HyperlinkedModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(view_name='variable-state-detail')
    variable = serializers.HyperlinkedRelatedField(view_name='variable-detail',
                                                   queryset=Variable.objects.all(),
                                                   many=False)
    owner = serializers.PrimaryKeyRelatedField(many=False, 
                                               queryset=User.objects.all(),
                                               read_only=False)
    
    class Meta:
        model = VariableState
        fields = ('url',
                  'id',
                  'index',
                  'label',
                  'kind',
                  'value',
                  'upper_bound',
                  'lower_bound',
                  'variable',
                  'owner',)