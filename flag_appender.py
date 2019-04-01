import os.path
from sys import argv
from collections import defaultdict
from abc import ABC, abstractmethod
import os

class FilenamesGenerator(ABC):
    @abstractmethod
    def generate(self, filename):
        pass

class IncludedFilenamesGenerator(FilenamesGenerator):

    """Docstring for IncludedFilenamesGenerator. """

    def __init__(self):
        """TODO: to be defined1. """
        self.file_dependency_mapper = defaultdict(list)
        self.keyword = "#include"
    def __search(self, filename):
        try:
            with open(filename, 'r') as file_buffer:
                self.__fill_file_dependency_mapper(file_buffer, filename)
        except FileNotFoundError:
            pass
    
    def __fill_file_dependency_mapper(self, file_buffer, filename):
        for line in file_buffer:
            if self.keyword in line:
                angled_or_quated_filename = line.split()[-1]
                trimed_filename = angled_or_quated_filename[1:-1]

                normalize_redundant_path = os.path.normpath(trimed_filename)
                root_dir = os.path.dirname(filename)
                dependent_abs_path = os.path.join(root_dir, normalize_redundant_path)

                self.file_dependency_mapper[filename].append(dependent_abs_path)
                self.__search(trimed_filename)

    def __fill_dependent_file_list(self, filename, dependent_file_list):
        for file in self.file_dependency_mapper[filename]:
            self.__fill_dependent_file_list(file, dependent_file_list)
            dependent_file_list.append(file)

        return dependent_file_list
    
    def generate(self, filename):
        dependent_file_list = []
        self.__search(filename)
        self.__fill_dependent_file_list(filename, dependent_file_list)
        self.file_dependency_mapper.clear()

        return dependent_file_list

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
        super().__init__( AbsolutePathGenerator( IncludedFilenamesGenerator() ) )
        self.flag = flag

    def generate_flags(self, dependent_file_list):
        flaged_files = [ self.flag + filename for filename in dependent_file_list ]
        
        return flaged_files

class AbsolutePathGenerator(FilenamesGenerator):
    """Docstring for FilePathFinder. """

    def __init__(self, filenames):
        """TODO: to be defined1. """
        self.filenames = filenames
    
    def generate(self, filename):
        files = self.filenames.generate(filename);
        absolute_paths = [ os.path.abspath(file) for file in files if os.path.exists(file) ]
        
        return absolute_paths

    def __search():
        pass

flagAppender = PrependedFlagGenerator("-I")
print( flagAppender.generate( argv[1] ) )
