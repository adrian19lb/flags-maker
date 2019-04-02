from abc import ABC, abstractmethod
from filepathsgenerator import filepaths_generator

class FlagGenerator(ABC):
    """Docstring for FlagGenerator. """

    def __init__(self, filenames_holder):
        """TODO: to be defined1. """
        self.filenames_holder = filenames_holder
    
    def generate(self, filename):
        dependent_file_list = self.filenames_holder.generate(filename)
        
        return self.generate_flags(dependent_file_list)

    @abstractmethod
    def generate_flags(self, dependent_file_list):
        return

class PrependedFlagGenerator(FlagGenerator):
    def __init__(self, flag):
        super().__init__( filepaths_generator.AbsolutePathGenerator( filepaths_generator.IncludedFilenamesGenerator() ) )
        self.flag = flag

    def generate_flags(self, dependent_file_list):
        flaged_files = [ self.flag + filename for filename in dependent_file_list ]
        
        return flaged_files
