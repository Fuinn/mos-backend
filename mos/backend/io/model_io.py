from .parser import ModelParser

class ModelIO:
    
    ANNOTATION_TAG = '#@'

    def read(self, filepath, owner):

        parser = ModelParser(self.ANNOTATION_TAG)
        parser.parse(filepath)
        return parser.build_model(owner)    

    def write(self, model, file, base_path=''):
        """
        Writes model to file.

        Parameters
        ----------
        model : |Model|
        file : File
        base_path : base path for input files (string)
        """

        raise NotImplementedError()
    