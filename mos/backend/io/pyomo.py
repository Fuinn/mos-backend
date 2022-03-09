import os
import re
import json
from .model_io import ModelIO

from django.conf import settings

class PyomoModelIO(ModelIO):

    def write(self, model, file, base_path):

        input_files = model.interface_files.filter(type='input').all()
        input_objects = model.interface_objects.filter(type='input').all()

        for line in model.source.splitlines():
            
            # Input files
            for f in input_files:
                pattern = re.compile("%s\s*=" %f.name)
                if pattern.match(line):
                    readtype = 'r'
                    local_path = os.path.join(settings.MEDIA_ROOT, f.data.name)
                    try:
                        with open(local_path, 'r') as ff:
                            ff.readline()
                    except UnicodeDecodeError:
                        readtype = 'rb'
                    line = "%s = '%s'" %(f.name, os.path.join(base_path, f.name+f.extension))
                    break

            # Input objects
            for o in input_objects:
                pattern = re.compile("%s\s*=" %o.name)
                if pattern.match(line):
                    line = "%s = json.load(open('%s', 'r'))" %(o.name, 
                                                               os.path.join(base_path,
                                                                            o.name+'.json'))
                    break

            # Write
            file.write(line+os.linesep)
