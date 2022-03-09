from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'model', views.ModelViewSet, basename='model')
router.register(r'interface-file', views.InterfaceFileViewSet, basename='interface-file')
router.register(r'interface-object', views.InterfaceObjectViewSet, basename='interface-object')
router.register(r'helper-object', views.HelperObjectViewSet, basename='helper-object')
router.register(r'variable', views.VariableViewSet, basename='variable')
router.register(r'variable-state', views.VariableStateViewSet, basename='variable-state')
router.register(r'function', views.FunctionViewSet, basename='function')
router.register(r'function-state', views.FunctionStateViewSet, basename='function-state')
router.register(r'constraint', views.ConstraintViewSet, basename='constraint')
router.register(r'constraint-state', views.ConstraintStateViewSet, basename='constraint-state')
router.register(r'problem', views.ProblemViewSet, basename='problem')
router.register(r'problem-state', views.ProblemStateViewSet, basename='problem-state')
router.register(r'solver', views.SolverViewSet, basename='solver')
router.register(r'solver-state', views.SolverStateViewSet, basename='solver-state')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^authenticate/', views.CustomObtainAuthToken.as_view()),
    url(r'^signup/', views.UserSignUpView.as_view()),
]
