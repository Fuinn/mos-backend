from django.db import models
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class Solver(models.Model):

    name = models.CharField(default='', max_length=100)
    
    model = models.OneToOneField('Model',
                                 related_name='solver',
                                 on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='solvers',
                              on_delete=models.CASCADE)

    def has_state(self): 
        
        return hasattr(self, 'state') and self.state is not None

class SolverState(models.Model):

    name = models.CharField(default='Unknown', max_length=100)

    status = models.CharField(max_length=100)

    message = models.TextField(default='', blank=True)

    iterations = models.IntegerField(default=0)

    time = models.FloatField(default=0.)

    parameters = JSONField(default=dict)

    solver = models.OneToOneField('Solver',
                                  related_name='state',
                                  on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='solver_states',
                              on_delete=models.CASCADE)

class SolverSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='solver-detail')

    state = serializers.SerializerMethodField()

    model = serializers.HyperlinkedRelatedField(view_name='model-detail',
                                                read_only=True,
                                                many=False)

    def get_state(self, obj):

        return '{}?solver={}'.format(reverse('solver-state-list',
                                             request=self.context['request']),
                                     obj.id)
     
    class Meta:
        model = Solver
        fields = ('url',
                  'id',
                  'name',
                  'model',
                  'state',)

class SolverStateSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='solver-state-detail')
    solver = serializers.HyperlinkedRelatedField(view_name='solver-detail',
                                                 queryset=Solver.objects.all(),
                                                 many=False)
    owner = serializers.PrimaryKeyRelatedField(many=False, 
                                               queryset=User.objects.all(),
                                               read_only=False)

    class Meta:
        model = SolverState
        fields = ('url',
                  'id',
                  'name',
                  'status',
                  'message',
                  'iterations',
                  'time',
                  'parameters',
                  'solver',
                  'owner',)
