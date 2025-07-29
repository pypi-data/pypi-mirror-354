import os
import glob
import subprocess
from filelock import FileLock
from omegaconf import OmegaConf
from pprint import pprint
import shutil

from file_golem._file_io_helper import _does_path_exist, \
    _initialize_load_save_extension_dicts
from file_golem.file_datatypes import FileDatatypes, FilePathEntries, AbstractDatatype,SpecialDataArgs
from file_golem.config_datatype import Config
from file_golem.class_handler import ClassHandler
from datetime import datetime


class FileIO:
    DATA_DIRECTORY_NAME = 'data_directory_name'
    PROJECT_BASE_DIRECTORY = 'base_data_directory'
    FILELOCK_TIMEOUT_KEY = 'filelock_timeout'
    MAX_INDEXED_DIRECTORY_SIZE = 'max_indexed_directory_size'
    SYSTEM_TRANSFERS = 'system_transfers'
    PROJECT_SRC_ROOT = 'project_src_root'
    HAS_DUPLICATE_MODULE_NAMES = 'has_duplicate_module_names'
    SYSTEM_IDENTITY_FILE = 'system_identity_file'
    def __init__(self, system_config = None, system_config_path = None,is_debug=False, system_transfer=None):
        
        self.system_config = system_config
        self.system_config_path = system_config_path
        self.system_transfer = system_transfer
        #self.transfer_path_prefix = []

        self.is_debug = is_debug
        self.lengths_cache = {}
        self.config_cache = {}
        self.load_system_config()

        self.base_data_directory_name = self.system_config.get(self.DATA_DIRECTORY_NAME, 'data')

        self.class_handler = ClassHandler(
            self.system_config.get(self.PROJECT_SRC_ROOT, 'src'),
            self.system_config.get(self.HAS_DUPLICATE_MODULE_NAMES, False),
        )


        
        self.load_function_dict, \
        self.save_function_dict, \
        self.file_extension_dict, = _initialize_load_save_extension_dicts(self.system_config[SpecialDataArgs.SUPPORTED_FILETYPES.value])



    def load_system_config(self):
        if self.system_config_path is None:
            raise Exception('You must pass either a system_config or system_config_path to the FileIO constructor')
        
        self.load_function_dict, \
        self.save_function_dict, \
        self.file_extension_dict = _initialize_load_save_extension_dicts([FileDatatypes.OMEGA_CONF.value])

        #self.system_identity = None
        #self.system_paths_dict = {}
        self.system_config = self.load_config(self.system_config_path)

        ####Extract system identity and paths from the system config
        system_identity_file = self.system_config.get(self.SYSTEM_IDENTITY_FILE, '.system_identity.txt')
        with open(system_identity_file, 'r') as system_identity_file:
            self.system_identity = system_identity_file.read().strip()
        if self.is_debug:
            print(f'System Identity: {self.system_identity}')

        system_paths_dict = self.system_config.get(SpecialDataArgs.SYSTEM_PATHS.value, {})
            
        if self.system_transfer is None:
            self.absolute_path_prefix = system_paths_dict.get(self.system_identity,{}
                ).get(self.PROJECT_BASE_DIRECTORY, None).split(os.sep)
            if self.absolute_path_prefix is None:
                raise Exception(f'Base data directory not found in system config for system identity {self.system_identity}. Please specify it under {SpecialDataArgs.SYSTEM_PATHS.value}:{self.system_identity}:{self.PROJECT_BASE_DIRECTORY}')
            
        else:
            self.absolute_path_prefix = system_paths_dict.get(self.system_identity,{}).get(
                self.SYSTEM_TRANSFERS,{}).get(self.system_transfer,None).split(os.sep)
            if self.absolute_path_prefix is None:
                raise Exception(f'Base data directory not found in system config for transfer {self.system_identity} to {self.system_transfer}. Please specify it under {SpecialDataArgs.SYSTEM_PATHS.value}:{self.system_identity}:{self.SYSTEM_TRANSFERS}:{self.system_transfer}:{self.system_transfer}')

            

    def load_config(self,config_path):
        config = self._load_config_recursive(config_path,[])
        return config
    

    def _load_config_recursive(self,config_path,ancestry):
        if config_path in self.config_cache:
            return self.config_cache[config_path]
        if config_path in ancestry:
            raise Exception(f'Cycle detected in config inheritance: {ancestry}')
        
        config =self.load_data(Config, data_args = {
            Config.CONFIG_NAME: config_path
        })

        if self.is_debug:
            print('Loaded config: ', config_path),
            pprint(OmegaConf.to_yaml(config))

        defaults_list = config.get(SpecialDataArgs.DEFAULTS.value,[])
        for default_config_path in defaults_list:
            default_config = self._load_config_recursive(default_config_path,ancestry+[config_path])
            config = OmegaConf.merge(default_config,config)
        
        self.config_cache[config_path] = config
        return config

    def _config_to_tuple_fn(self,config_path):
        cwd = os.getcwd()
        base_cwd = os.path.basename(cwd)
        path_parts = config_path.split(os.sep)
        indices = [i for i, part in enumerate(path_parts) if part == base_cwd]

        if len(indices) > 1:
            print(f'WARNING: config path: {config_path} has multiple instances of {base_cwd}. This may cause issues with config loading.'
                    'It is strongly recommended to have only one instance of the base directory name in the config path.')
        elif len(indices) == 1:                
            path_parts = path_parts[indices[-1]+1:]
        config_file_extension = f'.{self.file_extension_dict[FileDatatypes.OMEGA_CONF]}'
        if path_parts[-1].endswith(config_file_extension):
            path_parts[-1] = path_parts[-1][:-len(config_file_extension)]
        return tuple(path_parts)
    

    def fetch_subconfig(self, config, subconfig_keys):
        if isinstance(config, str):
            config  = self.load_config(config)

        subconfig = config
        for key in subconfig_keys:
            if key not in subconfig:
                return {}
            subconfig = subconfig[key]
            if isinstance(subconfig, str):
                subconfig = self.load_config(subconfig)

        
        return subconfig
    

    def fetch_config_field(self,config, subconfig_keys = [],is_required=True):
        subconfig = self.fetch_subconfig(config,subconfig_keys[:-1])
        if not subconfig:
            if is_required:
                raise Exception(f'No subconfig found for keys {subconfig_keys} in config {config}')
            else:
                return
            
        field = subconfig.get(subconfig_keys[-1],None)

        if field is None:
            if is_required:
                raise Exception(f'No field found for keys {subconfig_keys} in config {config}')
            else:
                return None
        return field
    

    def fetch_class_from_config(self,config,subconfig_keys = [],is_required=True):
        model_class = self.fetch_config_field(config, subconfig_keys=subconfig_keys,is_required=is_required)
        if model_class is None:
            if is_required:
                raise Exception(f'No class found for keys {subconfig_keys} in config {config}')
            else:
                return None
        return self.fetch_class(model_class)

    def fetch_class(self,model_class):
        return self.class_handler._locate_class(model_class)



    def load_data(self,data_type, data_args={}):
        data_path = self.get_data_path(data_type,data_args)

        return self._load_data_core(data_type, data_path)
    
    def _load_data_core(self,data_type, data_path):
        if self.is_debug:
            print('Loading data from',data_path)
        load_function = self.load_function_dict[data_type.FILE_DATATYPE]
        data = load_function(data_path)
        return data
    
    def save_data(self,data_type, data_args):
        data_path = self.get_data_path(data_type,data_args)
        self.create_directory(data_path)
        save_function = self.save_function_dict[data_type.FILE_DATATYPE]
        data = data_args[AbstractDatatype.DATA]
        if self.is_debug:
            print('Saving data to',data_path)
        save_function(data,data_path)

    def create_directory(self,path):
        dir_path = os.path.dirname(path)
        if len(dir_path) == 0:
            return
        if self.is_debug:
            if not os.path.exists(dir_path):
                print(f'Creating directory: {dir_path}')
        os.makedirs(dir_path,exist_ok=True)


    def transfer_data(self,source_datatype,target_datatype, source_data_args, target_data_args):
        source_path = self.get_data_path(source_datatype, data_args=source_data_args)
        target_path = self.get_data_path(target_datatype, data_args=target_data_args)
        self.create_directory(target_path)
        if self.is_debug:
            print(f'Overwriting {target_path} with data at {source_path}')
        shutil.copy(source_path, target_path)



    def delete_data(self,data_type, data_args):
        for file_path in self.get_file_iterator(data_type, data_args = data_args):
            if os.path.isdir(file_path):
                for root, dirs, files in os.walk(file_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(file_path)
            else:
                os.remove(file_path)


    def get_data_path(self,datatype,data_args,is_lock_file=False, is_from=None, is_to=None):

        #Build the relative path
        relative_path_list = self._build_relative_path_list(datatype,data_args)
        if datatype.FILE_DATATYPE is not FileDatatypes.EMPTY:
            if datatype.FILE_DATATYPE not in self.file_extension_dict:
                raise Exception(f'File datatype {datatype.FILE_DATATYPE.value} not found in file extension dict. Please check the supported filetypes in the system config.')
            file_extenion = self.file_extension_dict[datatype.FILE_DATATYPE]
            relative_path_list[-1] += f'.{file_extenion}'
        
        if is_lock_file:
            relative_path_list[-1] += '.lock'

        path_prefix = self._get_path_prefix(datatype, is_from, is_to)


        complete_path =  os.path.join( *path_prefix, *relative_path_list)
        if not complete_path.startswith(os.sep):
            complete_path = os.sep + complete_path

        complete_path = self._resolve_symlinks(complete_path)
        #return complete_path

        normed_path = os.path.normpath(complete_path)
        return normed_path
    

    def _resolve_symlinks(self, path):
        if self.system_transfer is None:
            return path
        if self.is_debug:
            print(f'Due to system transfer, resolving symlinks for path: {path}')
        symlink_set = set()
        path = self._resolve_symlinks_recursive(path,symlink_set)
        return path


    def _resolve_symlinks_recursive(self,path,symlink_set):
        path_components = path.split(os.sep)
        #for i in range(len(path_components)-1):
        for i in range(len(path_components)):
            partial_path = '/'+ os.path.join(*path_components[:i+1])
            if os.path.islink(partial_path):
                if partial_path in symlink_set:
                    raise Exception(f'Cycle detected in symlinks: {partial_path} already visited')
                symlink_set.add(partial_path)


                symlink_target = os.readlink(partial_path)
                if self.is_debug:
                    print(f'Found symlink: {partial_path} to {symlink_target}')
                if os.path.isabs(symlink_target):
                    transfer_system_base_directory = self.system_config.get(
                        SpecialDataArgs.SYSTEM_PATHS.value, {}).get(
                        self.system_transfer, {}).get(
                        self.PROJECT_BASE_DIRECTORY, None)
                    relative_path = os.path.relpath(symlink_target, start=transfer_system_base_directory)

                else:
                    raise Exception(f'Symlink target {symlink_target} is not an absolute path. In this case, behavior is unknown. possibly set relative path to symlink target.')
                    relative_path = symlink_target

                unsymlinked_path = os.path.join(*self.absolute_path_prefix,relative_path,*path_components[i+1:])
                if not unsymlinked_path.startswith(os.sep):
                    unsymlinked_path = os.sep + unsymlinked_path
                return self._resolve_symlinks_recursive(unsymlinked_path, symlink_set)

        return path



    def _get_path_prefix(self,datatype,is_from, is_to):
        if datatype is Config:
            return os.getcwd().split(os.sep) #Config is always assumed to be in the current working directory
        
        #prefix = []
        prefix = self.absolute_path_prefix

        if (is_from is not None) and (is_to is not None):
            raise Exception('cannot specify both is_from and is_to')
        elif (is_from is not None) or (is_to is not None):
            shortest_path = self.get_entry_point_path(is_from,is_to)
            prefix += shortest_path.split(os.sep)

        return prefix

        # raise Exception('fix here')

        # if self.system_transfer is not None:
        #     prefix += self.transfer_path_prefix        
        # return prefix
    
    def atomic_operation(self,datatype,data_args,atomic_function,new_data):
        data_lock_path = self.get_data_path(datatype, data_args=data_args,is_lock_file=True)
        if self.is_debug:
            print(f'Creating filelock at {data_lock_path}')
        #timeout = self.system_config[self.FILELOCK_TIMEOUT_KEY]
        timeout = self.system_config.get(self.FILELOCK_TIMEOUT_KEY, 60)
        filelock = FileLock(data_lock_path, timeout=timeout)
        filelock.acquire()
        if self.is_file_present(datatype, data_args=data_args):
            data = self.load_data(datatype,data_args=data_args)
        else:
            data = None
        modified_data = atomic_function(data,new_data)
        data_args[AbstractDatatype.DATA] = modified_data
        self.save_data(datatype, data_args)

        os.remove(data_lock_path)
        filelock.release()
        if self.is_debug:
            print(f'Released and deleted filelock at {data_lock_path}')
        

    def get_file_iterator(self, data_type, data_args):
        partial_path = self.get_data_path(data_type,data_args)
        for file in glob.glob(partial_path,recursive=True):
            yield file
        
    def get_data_iterator(self, data_type, data_args):
        for file_path in self.get_file_iterator(data_type, data_args):
            data = self._load_data_core(data_type, file_path)
            yield data

    def _build_relative_path_list(self,datatype,data_args):
        relative_path_list = []
        for entry in datatype.RELATIVE_PATH_TUPLE:
            if entry == FilePathEntries.BASE_DATA_DIRECTORY:
                relative_path_list.append(self.base_data_directory_name)
            elif entry == FilePathEntries.IDX_ENTRY:
                idx = data_args[AbstractDatatype.IDX]
                if idx == FilePathEntries.OPEN_ENTRY:
                    relative_path_list.append('**')
                else:
                    relative_path_list.append(str(idx))
            elif entry == FilePathEntries.MODULATED_IDX_ENTRY:
                max_idx = self.system_config.get(self.MAX_INDEXED_DIRECTORY_SIZE, 10000)
                raise Exception('Modulated idx entry is not implemented yet')
            elif entry == FilePathEntries.CONFIG_ENTRY:
                config_name = data_args[AbstractDatatype.CONFIG_NAME]
                if config_name is None:
                    raise Exception(f'Config name not found in data args: {data_args}')
                if config_name == FilePathEntries.OPEN_ENTRY:
                    relative_path_list.append('**')
                else:
                    relative_config_tuple = self._config_to_tuple_fn(config_name)
                    relative_path_list.extend(relative_config_tuple)
            elif entry == FilePathEntries.TIMESTAMP_CONFIG_ENTRY:
                config_name = data_args[AbstractDatatype.CONFIG_NAME]
                if config_name is None:
                    raise Exception(f'Config name not found in data args: {data_args}')
                if config_name == FilePathEntries.OPEN_ENTRY:
                    relative_path_list.append('*')
                else:
                    relative_config_tuple = self._config_to_tuple_fn(config_name)
                    timestamp = datetime.now().strftime('%m-%d_%H:%M:%S')
                    relative_path_list.append(f'{relative_config_tuple[-1]}_{timestamp}')
            elif entry == FilePathEntries.DATA_TYPE_ENTRY:
                data_type_entry = datatype.__class__.__name__
                relative_path_list.append(data_type_entry)
            elif isinstance(entry, dict):
                if len(entry) != 1:
                    raise Exception(f'Dictionary entry in RELATIVE_PATH_TUPLE must have exactly one key-value pair, but got: {entry}')
                key, value = next(iter(entry.items()))
                if key == FilePathEntries.DATA_ARG_ENTRY:
                    field = data_args[value]
                    if field == FilePathEntries.OPEN_ENTRY:
                        relative_path_list.append('*')
                    else:
                        relative_path_list.append(str(field))
                elif key == FilePathEntries.CUSTOM_LOGIC:
                    custom_fn = getattr(datatype,value)
                    data_args[SpecialDataArgs.DATA_IO]=self
                    data_args[SpecialDataArgs.DATA_TYPE]=datatype
                    custom_values = custom_fn(data_args)

                    if custom_values is FilePathEntries.OPEN_ENTRY:
                        custom_values = ['*']
                    if isinstance(custom_values, str):
                        custom_values = [custom_values]
                    relative_path_list.extend(custom_values)
                elif key == FilePathEntries.ATTRIBUTE_ENTRY:
                    attribute = getattr(datatype,value)
                    relative_path_list.append(str(attribute))
                elif key == FilePathEntries.ZERO_PADDED_IDX_ENTRY:
                    idx = data_args[AbstractDatatype.IDX]
                    if idx == FilePathEntries.OPEN_ENTRY:
                        relative_path_list.append('*')
                    else:
                        zero_padded_idx = str(idx).zfill(value)
                        relative_path_list.append(zero_padded_idx)
                else:
                    raise Exception(f'Invalid key in dictionary entry in RELATIVE_PATH_TUPLE: {key}')
            elif isinstance(entry, str):
                relative_path_list.append(entry)
            else:
                raise Exception(f'Invalid entry in RELATIVE_PATH_TUPLE: {entry}')
        return relative_path_list


    def retrieve_data_args(self,data_type,partial_data_args, data_path):
        #TODO: FIX TO BE GENERAL
        relative_path_list = data_path.split(os.sep)

        epoch = relative_path_list[-1].split('.')[0]
        missing_data_args = {
            'epoch': epoch
        }
        return missing_data_args

    def get_datatype_length(self,datatype, data_args={}):
        if datatype in self.lengths_cache:
            length = self.lengths_cache[datatype]
        else:
            if datatype.LENGTH == -1:
                data_args[SpecialDataArgs.DATA_IO]=self
                data_args[SpecialDataArgs.DATA_TYPE]=datatype
                length = datatype._custom_length_logic(data_args)
            else:
                length = datatype.LENGTH
            self.lengths_cache[datatype] = length
        return length    

        
    def _get_config_directory(self):
        config_directory_key = 'config_directory'
        if config_directory_key in self.system_config:
            return self.system_config[config_directory_key]
        else:
            raise Exception(f'{config_directory_key} found in system config ({self.system_config_path})')
    
    def is_file_present(self,data_type,data_args):
        data_path = self.get_data_path(data_type,data_args)
        if self.is_debug:
            print('Checking if file is present at',data_path)
        is_file_present = _does_path_exist(data_path)
        return is_file_present
    

    def run_system_command(self,command):
        if self.is_debug:
            print('Running terminal command:',command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        for line in process.stdout:
            print(line, end='')
        process.wait()

    def execute_python_command(self,entry_point_name, args_dict):
        cd_path = self.get_entry_point_path(is_to=entry_point_name)
        conda_path = self.get_conda_path(entry_point_name)
        python_entry_file = self.system_config.get(
            SpecialDataArgs.SYSTEM_PATHS.value, {}).get(
            self.system_identity, {}).get(
            SpecialDataArgs.EXTERNAL_CALLS.value, {}).get(
            entry_point_name, {}).get(
            SpecialDataArgs.PYTHON_ENTRY_POINT.value, None)
        if python_entry_file is None:
            raise Exception(f'Python entry point for {entry_point_name} not found in system config for system identity {self.system_identity}')
        args_string = ''
        for key, value in args_dict.items():
            if value is None:
                args_string += f' --{key}'
            else:
                args_string += f' --{key} {value}'
        cmmd_string = (
            f'cd {cd_path} && {conda_path} {python_entry_file}.py {args_string}'
        )
        self.run_system_command(cmmd_string)

    def get_conda_path(self,entry_point_name):
        conda_path = self.system_config.get(
            SpecialDataArgs.SYSTEM_PATHS.value, {}).get(
            self.system_identity, {}).get(
            SpecialDataArgs.EXTERNAL_CALLS.value, {}).get(
            entry_point_name, {}).get(
            SpecialDataArgs.CONDA_PATH.value, None)
        
        conda_path = os.path.join(conda_path, 'bin', 'python')
        if conda_path is None:
            raise Exception(f'Conda path {entry_point_name} not found in system config for system identity {self.system_identity}')
        return conda_path
    
    def get_entry_point_path(self,is_from=None, is_to=None):
        #TODO: Should deprecate in favor of using abbsolute paths 
        if (is_from is not None) and (is_to is not None):
            raise Exception('cannot specify both is_from and is_to')
        elif is_from is None and is_to is None:
            raise Exception('must specify either is_from or is_to')
        
        entry_point_name = is_from if is_from is not None else is_to
        entry_point_path = self.system_config.get(
            SpecialDataArgs.SYSTEM_PATHS.value, {}).get(
            self.system_identity, {}).get(
            SpecialDataArgs.EXTERNAL_CALLS.value, {}).get(
            entry_point_name, {}).get(
            SpecialDataArgs.ENTRY_POINT.value, None)
        
        if entry_point_path is None:
            raise Exception(f'Entry point {entry_point_name} not found in system config for system identity {self.system_identity}')
        
        cwd = os.getcwd()
        if is_to is not None:
            relpath = os.path.relpath(entry_point_path, cwd)
        else:
            relpath = os.path.relpath(cwd, entry_point_path)
        

        return relpath