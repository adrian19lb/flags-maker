from abc import ABC, abstractmethod
from filepathsgenerator import filepaths_generator

class FlagGenerator(ABC):
    """
    Abstract base class for flags generators implementation. All classes, which inherit from
    this one must override generate_flags() method
        
    Args:
        filenames_holder(FilenamesGenerator): Given container with filepaths mapper. This arg 
        will be used for compute flags 

    Attributes:
        filenames_holder(FilenamesGenerator): Internal variable to store FilenamesGenerator 
    """

    def __init__(self, filenames_holder):
        self.filenames_holder = filenames_holder
    
    def generate(self, filename):
        """ Generate flags by given filename and dependent filenames
            
            Args: 
                filename(str): Name of file
            Raises:
                NoFileError: File doesn't exist
            Returns:
                created_flag
        """
        dependent_file_list = self.filenames_holder.generate(filename)
        
        return self.generate_flags(dependent_file_list)

    @abstractmethod
    def generate_flags(self, dependent_file_list):
        """ Abstract method for implementation of way generating flags
        """
        return

class PrependedFlagGenerator(FlagGenerator):
    def __init__(self, flag):
        super().__init__( filepaths_generator.AbsolutePathGenerator( filepaths_generator.IncludedFilenamesGenerator() ) )
        self.flag = flag

    def generate_flags(self, dependent_file_list):
        flaged_files = [ self.flag + filename for filename in dependent_file_list ]
        
        return flaged_files
