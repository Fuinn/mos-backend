import os
import re
import json

from .model_io import ModelIO

class GamsModelIO(ModelIO):

    ANNOTATION_TAG = '*@'

    def write(self, model, file, base_path):

        input_files = model.interface_files.filter(type='input').all()
        input_objects = model.interface_objects.filter(type='input').all()

        for line in model.source.splitlines():
            
            # Input files
            for f in input_files:
                pattern1 = re.compile("^\$include")
                pattern2 = re.compile("^\$gdxin")
                if (pattern1.match(line) or pattern2.match(line)) and f.name+f.extension in line:
                    if f.extension == '.gdx':
                        line = "$gdxin %s" %(os.path.join(base_path, f.name+f.extension))
                    else:
                        line = "$include %s" %(os.path.join(base_path, f.name+f.extension))
                    break

            # Input objects
            for o in input_objects:
                pattern = re.compile("^Scalar %s" %o.name)
                if pattern.match(line):
                    line = "Scalar %s /%s/;" %(o.name, json.dumps(o.data))
                    break

            # Write
            file.write(line+os.linesep)
