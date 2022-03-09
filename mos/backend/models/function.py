from django.db import models
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class Function(models.Model):

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

    # Objective choices
    OBJ_MINIMIZE = 'minimize',
    OBJ_MAXIMIZE = 'maximize',
    OBJ_NONE = 'none'
    OBJ_CHOICES = [
        (OBJ_MINIMIZE, 'Minimize'),
        (OBJ_MAXIMIZE, 'Maximize'),
        (OBJ_NONE, 'None')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(default='No description')
    labels = models.CharField(max_length=100, default='', blank=True)
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_UNKNOWN, max_length=100)
    shape = JSONField(blank=True, null=True) # None for scalar/unknown
                                             # List of one element for hashmap
                                             # List of multiple elements for array 

    objective = models.CharField(choices=TYPE_CHOICES,
                                 default=TYPE_UNKNOWN,
                                 max_length=100)
   

    model = models.ForeignKey('Model',
                              related_name='functions',
                              on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='functions',
                              on_delete=models.CASCADE)

class FunctionState(models.Model):

    index = JSONField(blank=True, null=True)
    label = models.CharField(default="", blank=True, max_length=200)
    value = models.FloatField(default=0.)
    function = models.ForeignKey('Function',
                                 related_name='states',
                                 on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='function_states',
                              on_delete=models.CASCADE)
        
class FunctionSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='function-detail')
    states = serializers.SerializerMethodField()
    model = serializers.HyperlinkedRelatedField(view_name='model-detail',
                                                read_only=True,
                                                many=False)

    def get_states(self, obj):

        return '{}?function={}'.format(reverse('function-state-list',
                                               request=self.context['request']),
                                        obj.id)
                                                
    class Meta:
        model = Function
        fields = ('url',
                  'id',
                  'name',
                  'description',
                  'labels',
                  'type',
                  'shape',
                  'objective',
                  'states',
                  'model',)

class FunctionStateSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='function-state-detail')
    function = serializers.HyperlinkedRelatedField(view_name='function-detail',
                                                   queryset=Function.objects.all(),
                                                   many=False)
    owner = serializers.PrimaryKeyRelatedField(many=False, 
                                               queryset=User.objects.all(),
                                               read_only=False)
    
    class Meta:
        model = FunctionState
        fields = ('url',
                  'id',
                  'index',
                  'label',
                  'value',
                  'function',
                  'owner',)
