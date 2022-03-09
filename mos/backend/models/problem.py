from django.db import models
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

class Problem(models.Model):

    name = models.CharField(max_length=100)

    model = models.OneToOneField('Model',
                                 related_name='problem',
                                 on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='problems',
                              on_delete=models.CASCADE)

    def has_state(self):
        
        return hasattr(self, 'state') and self.state is not None

class ProblemState(models.Model):

    # Kind choices
    KIND_LP = 'lp'
    KIND_NLP = 'nlp'
    KIND_MILP = 'milp'
    KIND_CONVEX = 'convex'
    KIND_INTEGER = 'mip'
    KIND_MCP = 'mcp'
    KIND_UNKNOWN = 'unknown'
    KIND_CHOICES = [
        (KIND_LP, 'Lp'),
        (KIND_NLP, 'Nlp'),
        (KIND_MILP, 'Milp'),
        (KIND_CONVEX, 'Convex'),
        (KIND_INTEGER, 'mip'),
        (KIND_MCP, 'mcp'),                        
        (KIND_UNKNOWN, 'Unknown')
    ]

    kind = models.CharField(choices=KIND_CHOICES, default=KIND_UNKNOWN, max_length=100)

    num_vars = models.IntegerField(default=0)

    num_constraints = models.IntegerField(default=0)

    problem = models.OneToOneField('Problem',
                                   related_name='state',
                                   on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User',
                              related_name='problem_states',
                              on_delete=models.CASCADE)

class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(view_name='problem-detail')

    state = serializers.SerializerMethodField()

    model = serializers.HyperlinkedRelatedField(view_name='model-detail', 
                                                read_only=True,
                                                many=False)

    def get_state(self, obj):

        return '{}?problem={}'.format(reverse('problem-state-list',
                                              request=self.context['request']),
                                      obj.id)
    
    class Meta:
        model = Problem
        fields = ('url',
                  'id',
                  'name',
                  'model',
                  'state',)

class ProblemStateSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='problem-state-detail')
    problem = serializers.HyperlinkedRelatedField(view_name='problem-detail',
                                                  queryset=Problem.objects.all(),
                                                  many=False)
    owner = serializers.PrimaryKeyRelatedField(many=False, 
                                               queryset=User.objects.all(),
                                               read_only=False)

    class Meta:
        model = ProblemState
        fields = ('url',
                  'id',
                  'kind',
                  'num_vars',
                  'num_constraints',
                  'problem',
                  'owner',)
