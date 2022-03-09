import os
import io
import json
import datetime as dt
from contextlib import redirect_stderr, redirect_stdout

from django.conf import settings
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect

from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from . import models
from .rabbit import get_connection

### User
########

class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response(
            {'key': token.key, 
             'user_id': token.user_id,
             'username': token.user.username})

class UserSignUpView(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = models.UserSignUpSerializer

    def create(elf, request, *args, **kwargs):
        serializer = models.UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ready for sending email
        msg = """
        Dear MOS Admin,
        
        The following user has requested an MOS account:

        Email: {email}
        First Name: {fname}
        Last Name: {lname}
        Company: {company}

        Sincerely,
        MOS Backend
        """.format(
            email=serializer.validated_data['email'],
            fname=serializer.validated_data['first_name'],
            lname=serializer.validated_data['last_name'],
            company=serializer.validated_data['company'],
        )
        send_mail(
            'MOS User Account Request',
            msg,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

### Model
#########

class ModelViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.ModelSerializer
    
    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = models.Model.objects.all()
        else:
            queryset = models.Model.objects.filter(owner=self.request.user)
        queryset = queryset.order_by('owner__username', 'name', 'time_start')

        # Name
        if 'name' in self.request.query_params:
            queryset = queryset.filter(name=self.request.query_params.get('name'))

        return queryset

    def list(self, request):
        qs = self.get_queryset()
        serializer = models.ModelOverviewSerializer(qs, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_from_file(self, request):

        source_file = request.FILES['source_file']
        
        local_file = os.path.join(settings.MEDIA_ROOT,
                                  default_storage.save(source_file.name,
                                                       ContentFile(source_file.read())))

        s = io.StringIO()
        with redirect_stdout(s):
            try:
                model = models.Model.create_from_file(local_file, request.user)
                model = models.ModelSerializer(model, context={'request': request}).data
                print('Upload done')
            except Exception as e:
                model = None
                print('Error: %s' %str(e))

        print(s.getvalue())

        default_storage.delete(local_file)

        return Response({
            'model': model,
            'log': s.getvalue(),
        })

    @action(detail=True, methods=['post'])
    def delete_results(self, request, pk=None):

        # Model
        if request.user.is_superuser:
            model = models.Model.objects.get(pk=pk)
        else:
            model = models.Model.objects.get(pk=pk, owner=request.user)

        # Clean up
        model.delete_results()

        # Response
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_status(self, request, pk=None):

        if request.user.is_superuser:
            model = models.Model.objects.get(pk=pk)
        else:
            model = models.Model.objects.get(pk=pk, owner=request.user)

        return Response(model.status)

    @action(detail=True, methods=['put'])
    def set_execution_log(self, request, pk=None):

        if request.user.is_superuser:
            model = models.Model.objects.get(pk=pk)
        else:
            model = models.Model.objects.get(pk=pk, owner=request.user)

        model.execution_log = request.data
        model.save() 

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def set_status(self, request, pk=None):

        if request.user.is_superuser:
            model = models.Model.objects.get(pk=pk)
        else:
            model = models.Model.objects.get(pk=pk, owner=request.user)

        model.status = request.data
        if request.data in [models.Model.STATUS_CREATED,
                            models.Model.STATUS_QUEUED]:
            model.time_start = None
            model.time_end = None
        elif request.data == models.Model.STATUS_RUNNING:
            model.time_start = dt.datetime.now(dt.timezone.utc)
            model.time_end = None
        elif request.data in [models.Model.STATUS_SUCCESS,
                            models.Model.STATUS_ERROR]:
            model.time_end = dt.datetime.now(dt.timezone.utc)
        else:
            raise ValueError('invalid model status')
        model.save() 

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):

        # Model
        if request.user.is_superuser:
            model = models.Model.objects.get(pk=pk)
        else:
            model = models.Model.objects.get(pk=pk, owner=request.user)

        # Clean up
        model.delete_results()

        # Status and log
        model.status = models.Model.STATUS_QUEUED
        model.execution_log = ''
        model.save()
        
        # Push notification (queued)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(request.user.id),
            {
                'type': 'mos_notification',
                'notification': 
                    {
                    'model_id': model.id,
                    'model_name': model.name,
                    'status': model.STATUS_QUEUED,
                }
            }
        )

        # Dispatch task
        connection = get_connection()
        channel = connection.channel()
        channel.queue_declare(queue='mos-python')
        channel.queue_declare(queue='mos-julia')
        channel.basic_publish(
            exchange='',
            routing_key='mos-julia' if model.system == model.SYSTEM_JUMP else 'mos-python',
            body=json.dumps({
                'model_id': model.id,
                'model_name': model.name,
                'caller_id': request.user.id,
            }))
        connection.close()

        # Response
        return Response(models.ModelSerializer(model, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def write(self, request, pk=None):

        if request.user.is_superuser:
            model = models.Model.objects.get(pk=pk)
        else:
            model = models.Model.objects.get(pk=pk, owner=request.user)

        if 'base_path' in request.query_params:
            base_path = request.query_params.get('base_path')
        else:
            base_path = ''

        recipe = io.StringIO()
        model.write(recipe, base_path=base_path)

        return Response(recipe.getvalue())

### Interface File
##################

class InterfaceFileViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.InterfaceFileSerializer

    def update(self, request, pk=None):   
        
        if request.user.is_superuser:
            f = models.InterfaceFile.objects.get(pk=pk)
        else:
            f = models.InterfaceFile.objects.get(pk=pk, owner=request.user)
        f.name = request.data.get('name', f.name)
        f.description = request.data.get('description', f.description)
        f.type = request.data.get('type', f.type)
        f.extension = request.data.get('extension', f.extension)
        if 'data_file' in request.FILES:
            f.data = request.FILES['data_file']
            f.data_size = request.FILES['data_file'].size
            f.extension = os.path.splitext(request.FILES['data_file'].name)[-1]
            f.filename = request.FILES['data_file'].name
        f.save()

        return Response(models.InterfaceFileSerializer(f, context={'request': request}).data)

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = models.InterfaceFile.objects.all()
        else:
            queryset = models.InterfaceFile.objects.filter(owner=self.request.user)

        # Model
        if 'model' in self.request.query_params:
            queryset = queryset.filter(model__pk=self.request.query_params.get('model'))

        # Type
        if 'type' in self.request.query_params:
            queryset = queryset.filter(type=self.request.query_params.get('type'))

        return queryset

    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):

        if request.user.is_superuser:
            f = models.InterfaceFile.objects.get(pk=pk)
        else:
            f = models.InterfaceFile.objects.get(pk=pk, owner=request.user)
        url = request.build_absolute_uri(f.data.url)
        return HttpResponseRedirect(url)

    @action(detail=True, methods=['get'])
    def url(self, request, pk=None):
        if request.user.is_superuser:
            f = models.InterfaceFile.objects.get(pk=pk)
        else:
            f = models.InterfaceFile.objects.get(pk=pk, owner=request.user)
        url = request.build_absolute_uri(f.data.url)
        return Response(url)

### Interface Object
####################

class InterfaceObjectViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.InterfaceObjectSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return models.InterfaceObject.objects.all()
        else:
            return models.InterfaceObject.objects.filter(owner=self.request.user)

    def update(self, request, pk=None):   
         
        if request.user.is_superuser: 
            o = models.InterfaceObject.objects.get(pk=pk)
        else:
            o = models.InterfaceObject.objects.get(pk=pk, owner=request.user)
        o.name = request.data.get('name', o.name)
        o.description = request.data.get('description', o.description)
        o.type = request.data.get('type', o.type)
        o.data = request.data.get('data', o.data)
        o.data_size = len(json.dumps(o.data).encode('utf-8'))
        o.save()

        return Response(models.InterfaceObjectSerializer(o, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):

        if request.user.is_superuser:
            o = models.InterfaceObject.objects.get(pk=pk)
        else:
            o = models.InterfaceObject.objects.get(pk=pk, owner=request.user)

        return Response(o.data)

### Helper Object
#################

class HelperObjectViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.HelperObjectSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return models.HelperObject.objects.all()
        else:
            return models.HelperObject.objects.filter(owner=self.request.user)

    def update(self, request, pk=None):   
         
        if request.user.is_superuser: 
            o = models.HelperObject.objects.get(pk=pk)
        else:
            o = models.HelperObject.objects.get(pk=pk, owner=request.user)
        o.name = request.data.get('name', o.name)
        o.description = request.data.get('description', o.description)
        o.type = request.data.get('type', o.type)
        o.data = request.data.get('data', o.data)
        o.data_size = len(json.dumps(o.data).encode('utf-8'))
        o.save()

        return Response(models.HelperObjectSerializer(o, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):

        if request.user.is_superuser:
            o = models.HelperObject.objects.get(pk=pk)
        else:
            o = models.HelperObject.objects.get(pk=pk, owner=request.user)

        return Response(o.data)

### Variable
############

class VariableViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.VariableSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return models.Variable.objects.all()
        else:
            return models.Variable.objects.filter(owner=self.request.user)

    def update(self, request, pk=None):   
        
        if request.user.is_superuser:
            v = models.Variable.objects.get(pk=pk)
        else:
            v = models.Variable.objects.get(pk=pk, owner=request.user)
        v.name = request.data.get('name', v.name)
        v.description = request.data.get('description', v.description)
        v.type = request.data.get('type', v.type)
        v.shape = request.data.get('shape', v.shape)
        v.labels = request.data.get('labels', v.labels)
        v.save()

        return Response(models.VariableSerializer(v, context={'request': request}).data)

class VariableStateViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.VariableStateSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = models.VariableState.objects.all()
        else:
            queryset = models.VariableState.objects.filter(owner=self.request.user)

        # Variable
        if 'variable' in self.request.query_params:
            queryset = queryset.filter(variable__pk=self.request.query_params.get('variable'))

        return queryset

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):

        serializer = models.VariableStateSerializer(data=request.data, 
                                                    context={'request': request},
                                                    many=True)

        if serializer.is_valid():
            states = [models.VariableState(**item) for item in serializer.validated_data]
            if (not request.user.is_superuser and
                any([s.owner != request.user for s in states])):
                return Response(status=status.HTTP_400_BAD_REQUEST)    
            models.VariableState.objects.bulk_create(states)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FunctionViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.FunctionSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return models.Function.objects.all()
        else:
            return models.Function.objects.filter(owner=self.request.user)

    def update(self, request, pk=None):
         
        if request.user.is_superuser:
            f = models.Function.objects.get(pk=pk)
        else:
            f = models.Function.objects.get(pk=pk, owner=request.user)
        f.name = request.data.get('name', f.name)
        f.description = request.data.get('description', f.description)
        f.type = request.data.get('type', f.type)
        f.shape = request.data.get('shape', f.shape)
        f.labels = request.data.get('labels', f.labels)
        f.save()

        return Response(models.FunctionSerializer(f, context={'request': request}).data)


class FunctionStateViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.FunctionStateSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = models.FunctionState.objects.all()
        else:
            queryset = models.FunctionState.objects.filter(owner=self.request.user)

        # Function
        if 'function' in self.request.query_params:
            queryset = queryset.filter(function__pk=self.request.query_params.get('function'))

        return queryset

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):

        serializer = models.FunctionStateSerializer(data=request.data, 
                                                    context={'request': request},
                                                    many=True)

        if serializer.is_valid():
            states = [models.FunctionState(**item) for item in serializer.validated_data]
            if (not request.user.is_superuser and
                any([s.owner != request.user for s in states])):
                return Response(status=status.HTTP_400_BAD_REQUEST)    
            models.FunctionState.objects.bulk_create(states)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ConstraintViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.ConstraintSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return models.Constraint.objects.all()
        else:
            return models.Constraint.objects.filter(owner=self.request.user)

class ConstraintStateViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.ConstraintStateSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = models.ConstraintState.objects.all()
        else:
            queryset = models.ConstraintState.objects.filter(owner=self.request.user)

        # Constraint
        if 'constraint' in self.request.query_params:
            queryset = queryset.filter(constraint__pk=self.request.query_params.get('constraint'))

        return queryset

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):

        serializer = models.ConstraintStateSerializer(data=request.data, 
                                                      context={'request': request},
                                                      many=True)

        if serializer.is_valid():
            states = [models.ConstraintState(**item) for item in serializer.validated_data]
            if (not request.user.is_superuser and
                any([s.owner != request.user for s in states])):
                return Response(status=status.HTTP_400_BAD_REQUEST)    
            models.ConstraintState.objects.bulk_create(states)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProblemViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.ProblemSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return models.Problem.objects.all()
        else:
            return models.Problem.objects.filter(owner=self.request.user)

class ProblemStateViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.ProblemStateSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = models.ProblemState.objects.all()
        else:
            queryset = models.ProblemState.objects.filter(owner=self.request.user)

        # Problem
        if 'problem' in self.request.query_params:
            queryset = queryset.filter(problem__pk=self.request.query_params.get('problem'))

        return queryset
    
class SolverViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.SolverSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            return models.Solver.objects.all()
        else:
            return models.Solver.objects.filter(owner=self.request.user)

class SolverStateViewSet(viewsets.ModelViewSet):
    
    serializer_class = models.SolverStateSerializer

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = models.SolverState.objects.all()
        else:
            queryset = models.SolverState.objects.filter(owner=self.request.user)

        # Solver
        if 'solver' in self.request.query_params:
            queryset = queryset.filter(solver__pk=self.request.query_params.get('solver'))

        return queryset