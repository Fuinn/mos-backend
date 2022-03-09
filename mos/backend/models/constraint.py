from django.db import models
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class Constraint(models.Model):

    # Constraint types
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
                              related_name='constraints',
                              on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='constraints',
                              on_delete=models.CASCADE)

class ConstraintState(models.Model):

    # Constraint kinds
    KIND_EQ = 'equality'
    KIND_INEQ = 'inequality'
    KIND_UNKNOWN = 'unknown'
    KIND_CHOICES = [
        (KIND_EQ, 'Equality'),
        (KIND_INEQ, 'Inequality'),
        (KIND_UNKNOWN, 'Unknown')
    ]

    index = JSONField(blank=True, null=True)
    label = models.CharField(default="", blank=True, max_length=200)
    kind = models.CharField(choices=KIND_CHOICES, max_length=100)
    dual = models.FloatField(default=0.)
    violation = models.FloatField(default=0.)
    constraint = models.ForeignKey('Constraint',
                                   related_name='states',
                                   on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='constraint_states',
                              on_delete=models.CASCADE)
    
class ConstraintSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='constraint-detail')
    states = serializers.SerializerMethodField()
    model = serializers.HyperlinkedRelatedField(view_name='model-detail',
                                                read_only=True,
                                                many=False)
                                                  
    
    def get_states(self, obj):

        return '{}?constraint={}'.format(reverse('constraint-state-list',
                                               request=self.context['request']),
                                        obj.id)

    class Meta:
        model = Constraint
        fields = ('url',
                  'id',
                  'name',
                  'description',
                  'labels',
                  'type',
                  'shape',
                  'states',
                  'model',)

class ConstraintStateSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='constraint-state-detail')
    constraint = serializers.HyperlinkedRelatedField(view_name='constraint-detail',
                                                     queryset=Constraint.objects.all(),
                                                     many=False)
    owner = serializers.PrimaryKeyRelatedField(many=False, 
                                               queryset=User.objects.all(),
                                               read_only=False)
    
    class Meta:
        model = ConstraintState
        fields = ('url',
                  'id',
                  'index',
                  'label',
                  'kind',
                  'dual',
                  'violation',
                  'constraint',
                  'owner',)
