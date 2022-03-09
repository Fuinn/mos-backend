import os
import datetime as dt

class ModelParser:

    def __init__(self, tag='#@'):

        self.source = ''
        self.model = None
        self.input_files = []
        self.input_objects = []
        self.helper_objects_pre = []
        self.variables = []
        self.functions = []
        self.constraints = []
        self.objective = None
        self.problem = None
        self.solver = None
        self.helper_objects_post = []
        self.output_files = []
        self.output_objects = []

        self.tag = tag
        self.file_ext = ''

    def __parse_annotation_body__(self, f, name=None):

        annotation = {}
        line = next(f)
        while True:
            if line[:2] == self.tag:
                line_split = line.split()
                key, value = line_split[1].lower(), line_split[2:]
                if key == 'description:':
                    annotation['description'] = ' '.join(value)
                elif key == 'labels:':
                    annotation['labels'] = value[0].strip() if value else ''
                else:
                    break
            else:
                break
            try:
                line = next(f)
            except StopIteration:
                line = None
                break

        if name is not None:
            annotation.update({'name': name})

        return annotation, line

    def __parse_annotation_header__(self, line):

        line = line[3:].split(':')
        token = line[0].lower()
        name = line[1] if len(line) > 1 else ''

        return token, name.strip()

    def parse(self, filepath):

        print('Parsing model file ...')
        print('Annotation tag %s' %self.tag)

        # Init
        pre = True
        self.__init__(tag=self.tag)

        # File
        f = open(filepath, 'r')

        # File extension
        self.file_ext = os.path.splitext(filepath)[-1]

        # Source
        self.source = f.read()
            
        # Initialize
        f.seek(0)
        try:
            line = next(f)
        except StopIteration:
            line = None

        # Process lines
        while line is not None:

            # Find annotation header
            while True:
                if line[:2] == self.tag:
                    break
                try:
                    line = next(f)
                except StopIteration:
                    line = None
                    break
            if line is None:
                break 

            # Parse annotation header
            assert(line[:2] == self.tag)
            token, name = self.__parse_annotation_header__(line)

            # Model
            if token == 'model':
                print('Model name "%s"' %name)
                try:
                    annotation, line  = self.__parse_annotation_body__(f, name)
                    self.model = annotation
                    print('Parsed model annotation')
                except Exception as e:
                    print('ERROR - Unable to parse model annotation')
                    raise e

            # Input file
            elif token == 'input file':
                try:
                    annotation, line = self.__parse_annotation_body__(f, name)
                    self.input_files.append(annotation)
                    print('Parsed input file "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse input file "%s"' %name)
                    raise e

            # Input object
            elif token == 'input object':
                try:
                    annotation, line = self.__parse_annotation_body__(f, name)
                    self.input_objects.append(annotation)
                    print('Parsed input object "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse input object "%s"' %name)
                    raise e

            # Helper object
            elif token == 'helper object':
                try:
                    annotation, line  = self.__parse_annotation_body__(f, name)
                    if pre:
                        self.helper_objects_pre.append(annotation)
                    else:
                        self.helper_objects_post.append(annotation)
                    print('Parsed helper object "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse helper object "%s"' %name)
                    raise e

            # Variable
            elif token == 'variable':
                try:
                    pre = False
                    annotation, line  = self.__parse_annotation_body__(f, name)
                    self.variables.append(annotation)
                    print('Parsed variable "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse variable "%s"' %name)
                    raise e

            # Function
            elif token == 'function':
                try:
                    pre = False
                    annotation, line  = self.__parse_annotation_body__(f, name)
                    self.functions.append(annotation)
                    print('Parsed function "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse function "%s"' %name)
                    raise e

            # Constraint
            elif token == 'constraint':
                try:
                    pre = False
                    annotation, line  = self.__parse_annotation_body__(f, name)
                    self.constraints.append(annotation)
                    print('Parsed constraint "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse constraint "%s"' %name)
                    raise e

            # Problem
            elif token == 'problem':
                try:
                    pre = False
                    annotation, line  = self.__parse_annotation_body__(f, name)
                    self.problem = annotation
                    print('Parsed problem "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse problem "%s"' %name)
                    raise e

            # Solver
            elif token == 'solver':
                try:
                    pre = False
                    annotation, line  = self.__parse_annotation_body__(f, name)
                    self.solver = annotation
                    print('Parsed solver "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse solver "%s"' %name)
                    raise e

            # Output file
            elif token == 'output file':
                try:
                    annotation, line = self.__parse_annotation_body__(f, name)
                    self.output_files.append(annotation)
                    print('Parsed output file "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse output file "%s"' %name)
                    raise e

            # Output object
            elif token == 'output object':
                try:
                    annotation, line = self.__parse_annotation_body__(f, name)
                    self.output_objects.append(annotation)
                    print('Parsed output object "%s"' %name)
                except Exception as e:
                    print('ERROR - Unable to parse output object "%s"' %name)
                    raise e

            # Invalid
            else:
                print('ERROR - Invalid token "%s"' %token)
                raise ValueError("Invalid token '%s'" %token)

        print('Model file parsed successfully!')

        f.close()

        return

    def get_system(self):

        from .. import models

        # File ext
        if self.file_ext == '.jl':
            return models.Model.SYSTEM_JUMP
        if self.file_ext == '.gms':
            return models.Model.SYSTEM_GAMS
                
        # In source
        for system, _ in models.Model.SYSTEM_CHOICES:
            if system in self.source:
                return system

        # I give up
        return 'unknown'

    def build_model(self, owner):

        from .. import models

        NO_DES = 'No description'

        print('Building model ...')

        # Model
        annotation = self.model if self.model is not None else {}
        model = models.Model.objects.create(owner=owner,
                                            name=annotation.get('name', 'New Model'),
                                            description=annotation.get('description', NO_DES),
                                            system=self.get_system(),
                                            source=self.source,
                                            time_created=dt.datetime.now())
        print('Built model container')

        # Interface files
        for i, files in enumerate([self.input_files, self.output_files]):
            for f in files:
                name, ext = os.path.splitext(f['name'])
                models.InterfaceFile.objects.create(name=name, 
                                                    owner=owner,
                                                    description=f.get('description', NO_DES),
                                                    type='input' if i == 0 else 'output',
                                                    extension=ext,
                                                    model=model)
                print('Added interface file "%s"' %name)

        # Interface objects
        for i, objects in enumerate([self.input_objects, self.output_objects]):
            for o in objects:
                models.InterfaceObject.objects.create(name=o['name'], 
                                                      owner=owner,
                                                      description=o.get('description', NO_DES),
                                                      type='input' if i == 0 else 'output',
                                                      model=model)
                print('Added interface object "%s"' %(o['name']))

        # Helper objects
        for i, objects in enumerate([self.helper_objects_pre, self.helper_objects_post]):
            for o in objects:
                models.HelperObject.objects.create(name=o['name'],
                                                   owner=owner, 
                                                   description=o.get('description', NO_DES),
                                                   type='pre' if i == 0 else 'post',
                                                   model=model)
                print('Added context object "%s"' %(o['name']))
        
        # Variables
        for v in self.variables:
            models.Variable.objects.create(name=v['name'],
                                           owner=owner,
                                           description=v.get('description', NO_DES),
                                           labels=v.get('labels', ''),
                                           model=model)
            print('Added variable "%s"' %(v['name']))

        # Functions
        for f in self.functions:
            models.Function.objects.create(name=f['name'],
                                           owner=owner,
                                           description=f.get('description', NO_DES),
                                           labels=f.get('labels', ''),
                                           model=model)
            print('Added function "%s"' %(f['name']))

        # Constraints
        for c in self.constraints:
            models.Constraint.objects.create(name=c['name'],
                                             owner=owner,
                                             description=c.get('description', NO_DES),
                                             labels=c.get('labels', ''),
                                             model=model)
            print('Added constraint "%s"' %(c['name']))

        # Problem
        if self.problem is not None:
            models.Problem.objects.create(name=self.problem['name'],
                                          owner=owner,
                                          model=model)
            print('Added problem "%s"' %(self.problem['name']))

        # Solver
        if self.solver is not None:
            models.Solver.objects.create(name=self.solver['name'],
                                         owner=owner,
                                         model=model)
            print('Added solver "%s"' %(self.solver['name']))

        print('Model built successfully!')

        # Return
        return model
