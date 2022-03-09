import os

from .optmod import OptmodModelIO
from .jump import JumpModelIO
from .cvxpy import CvxpyModelIO
from .gams import GamsModelIO
from .pyomo import PyomoModelIO

def new_model_io(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    source = open(filepath, 'r').read()
    if ext == '.py':
        if 'cvxpy' in source:
            return CvxpyModelIO()
        elif 'optmod' in source:
            return OptmodModelIO()
        elif 'pyomo' in source:
            return PyomoModelIO()
        else:
            raise ValueError('unknown Python modeling system')
    elif ext == '.jl':
        return JumpModelIO()
    elif ext == '.gms':
        return GamsModelIO()
    else:
        raise ValueError('unknown model file extension')
