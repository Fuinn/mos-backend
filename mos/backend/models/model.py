from django.db import models
from rest_framework import serializers

from .. import io
from .interface_file import InterfaceFileSerializer
from .interface_object import InterfaceObjectSerializer
from .helper_object import HelperObjectSerializer
from .variable import VariableSerializer
from .function import FunctionSerializer
from .constraint import ConstraintSerializer
from .problem import ProblemSerializer
from .solver import SolverSerializer
from .user import UserSerializer

class Model(models.Model):

    # System choices
    SYSTEM_OPTMOD = 'optmod'
    SYSTEM_JUMP = 'jump'
    SYSTEM_CVXPY = 'cvxpy'
    SYSTEM_GAMS = 'gams'
    SYSTEM_PYOMO = 'pyomo'    
    SYSTEM_CHOICES = [
        (SYSTEM_OPTMOD, 'Optmod'),
        (SYSTEM_JUMP, 'JuMP'),
        (SYSTEM_CVXPY, 'CVXPY'),        
        (SYSTEM_GAMS, 'GAMS'),
        (SYSTEM_PYOMO, 'Pyomo')                
    ]

    # Status choices
    STATUS_CREATED = 'created'
    STATUS_QUEUED = 'queued'
    STATUS_RUNNING = 'running'
    STATUS_SUCCESS = 'success'
    STATUS_UNKNOWN = 'unknown'
    STATUS_ERROR = 'error'
    STATUS_CHOICES = [
        (STATUS_CREATED, 'Created'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_UNKNOWN, 'Unknown'),
        (STATUS_ERROR, 'Error')
    ]

    owner = models.ForeignKey('auth.User',
                              related_name='models',
                              on_delete=models.CASCADE)

    name = models.CharField(default='New Model', max_length=100)

    description = models.TextField(default='No description')
    
    system = models.CharField(choices=SYSTEM_CHOICES,
                              max_length=100)

    status = models.CharField(default=STATUS_CREATED,
                              choices=STATUS_CHOICES,
                              max_length=100)

    source = models.TextField(default='')

    time_created = models.DateTimeField()
    time_start = models.DateTimeField(default=None, null=True)
    time_end = models.DateTimeField(default=None, null=True)

    execution_log = models.TextField(default='')

    @classmethod
    def create_from_file(self, filepath, owner):

        return io.new_model_io(filepath).read(filepath, owner)

    def delete_results(self):

        # Model
        self.status = self.STATUS_UNKNOWN
        self.time_start = None
        self.time_end = None
        self.execution_log = ''
        self.save()

        # Helper objects
        for o in self.helper_objects.all():
            o.object = None
            o.save()

        # Variables states
        for v in self.variables.all():
            v.type = v.TYPE_UNKNOWN
            v.shape = None
            v.save()
            v.states.all().delete()

        # Functions states
        for f in self.functions.all():
            f.states.all().delete()

        # Constraint states
        for c in self.constraints.all():
            c.states.all().delete()

        # Solver state
        if self.has_solver() and self.solver.has_state():
            self.solver.state.delete()

        # Problem state
        if self.has_problem() and self.problem.has_state():
            self.problem.state.delete()

        # Output files
        for f in self.interface_files.filter(type='output').all():
            assert(f.type == 'output')
            f.file = None
            f.save()

        # Output objects
        for o in self.interface_objects.filter(type='output').all():
            assert(o.type == 'output')
            o.object = None
            o.save()

    def has_problem(self):    
        return hasattr(self, 'problem') and self.problem is not None

    def has_solver(self):
        return hasattr(self, 'solver') and self.solver is not None

    def write(self, file, base_path=''):

        if self.system == self.SYSTEM_OPTMOD:
            model_io = io.OptmodModelIO()
        elif self.system == self.SYSTEM_JUMP:
            model_io = io.JumpModelIO()
        elif self.system == self.SYSTEM_CVXPY:
            model_io = io.CvxpyModelIO()
        elif self.system == self.SYSTEM_GAMS:
            model_io = io.GamsModelIO()
        elif self.system == self.SYSTEM_PYOMO:
            model_io = io.PyomoModelIO()
        else:
            raise ValueError('Unknown modeling system')

        return model_io.write(self, file, base_path=base_path)

class ModelSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='model-detail')
    owner = UserSerializer()
    helper_objects = HelperObjectSerializer(many=True, read_only=True)
    interface_objects = InterfaceObjectSerializer(many=True, read_only=True)
    interface_files = InterfaceFileSerializer(many=True, read_only=True)
    variables = VariableSerializer(read_only=True, many=True)
    functions = FunctionSerializer(read_only=True, many=True)
    constraints = ConstraintSerializer(read_only=True, many=True)
    problem = ProblemSerializer(read_only=True, many=False)
    solver = SolverSerializer(read_only=True, many=False)

    class Meta:
        model = Model
        fields = ('url',
                  'id',
                  'owner',
                  'name',
                  'description',
                  'system',
                  'status',
                  'source',
                  'time_created',
                  'time_start',
                  'time_end',
                  'execution_log',
                  'helper_objects',
                  'interface_objects',
                  'interface_files',
                  'variables',
                  'functions',
                  'constraints',
                  'problem',
                  'solver',)


class ModelOverviewSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='model-detail')
    owner = UserSerializer()

    class Meta:
        model = Model
        fields = ('url',
                  'id',
                  'owner',
                  'name',
                  'system',
                  'status',
                  'time_created',
                  'time_start',
                  'time_end')