from typing                                                 import List, Optional, Dict, Any

from memory_fs.file.actions.Memory_FS__File__Name import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from memory_fs.schemas.Schema__Memory_FS__File__Metadata import Schema__Memory_FS__File__Metadata
from osbot_utils.utils.Json import bytes_to_json

from memory_fs.file.File_FS import File_FS
from memory_fs.file.actions.File_FS__Exists import File_FS__Exists
from osbot_utils.type_safe.decorators.type_safe             import type_safe
from memory_fs.file.actions.Memory_FS__File__Paths          import Memory_FS__File__Paths
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File              import Schema__Memory_FS__File
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

# todo: I think most of these Memory_FS__* classes should be refactored to the Storage_FS__* classes
class Memory_FS__Data(Type_Safe):
    storage     : Memory_FS__Storage

    def paths(self, file_config : Schema__Memory_FS__File__Config):
        return Memory_FS__File__Paths(file__config=file_config)

    def file_fs__exists(self, file_config : Schema__Memory_FS__File__Config):
        return File_FS__Exists(file__config=file_config, storage=self.storage)

    @type_safe
    def exists(self, file_config : Schema__Memory_FS__File__Config) -> bool:
        return self.file_fs__exists(file_config).config()

    # @type_safe
    # def exists(self, file_config : Schema__Memory_FS__File__Config
    #             ) -> bool:                                                          # todo: see if we need to add the default path (or to have a separate "exists strategy")
    #     files = self.storage.files()
    #     for full_file_path in self.paths(file_config).paths():
    #         if full_file_path in files:                                             # todo: refactor since this is going to be platform specific (specially since we shouldn't circle through all files to see if the file exists)
    #             return True                                                         # we only check if we found one of them
    #     return False                                                                # if none were found, return False

    def exists_content(self, file_config : Schema__Memory_FS__File__Config) -> bool:
        return self.file_fs__exists(file_config).content()

    # @type_safe
    # def exists_content(self, file_config : Schema__Memory_FS__File__Config
    #              ) -> bool:
    #     content_files =  self.storage.content_data()
    #     for full_file_path in self.paths(file_config).paths__content():
    #         if full_file_path in content_files:
    #             return True
    #     return False

    # todo: this method should return a strongly typed class (ideally one from the file)
    def get_file_info(self, path : Safe_Str__File__Path                                        # Get file information (size, hash, etc.)
                       ) -> Optional[Dict[Safe_Id, Any]]:
        # file = self.storage.file(path)
        # if not file:
        #     return None

        file_fs = self.load(path)
        if not file_fs:
            return None
        config   = file_fs.config().file_config()
        metadata = file_fs.metadata()

        content_size = int(metadata.content__size)                                # Get size from metadata
        return {Safe_Id("exists")       : True                                          ,
                Safe_Id("size")         : content_size                                  ,
                Safe_Id("content_hash") : metadata.content__hash                   ,
                Safe_Id("timestamp")    : metadata.timestamp                       ,
                Safe_Id("content_type") : config.file_type.content_type.value      }

    def list_files(self, prefix : Safe_Str__File__Path = None                                  # List all files, optionally filtered by prefix
                    ) -> List[Safe_Str__File__Path]:                                           # todo: see if we need this method
        if prefix is None:
            return list(self.storage.storage_fs.files__paths())

        prefix_str = str(prefix)
        if not prefix_str.endswith('/'):
            prefix_str += '/'

        return [path for path in self.storage.files__paths()
                if str(path).startswith(prefix_str)]

    def load(self, path: Safe_Str__File__Path) -> File_FS: # todo: see if we should have this method, or if we do need this more generic load() method (maybe to allow the discovery of the file from one of the paths: config, content or metadata)
        return self.load__from_path__config(path)          #for now assume the path is Safe_Str__File__Path

    def load__from_path__config(self, path : Safe_Str__File__Path) -> File_FS:                 # Load a File_Fs object from a config path
        with self.storage.storage_fs as _:
            if _.file__exists(path):                                                # todo add a check if path is indeed a .config file
                file_bytes = _.file__bytes(path)
                file_json  = bytes_to_json(file_bytes)
                file_config = Schema__Memory_FS__File__Config.from_json(file_json)  # todo: add error handling and the cases when file_json is not Schema__Memory_FS__File__Config
                file_fs     = File_FS(file_config=file_config, storage=self.storage)
                return file_fs


    # def load_content(self, path : Safe_Str__File__Path                                         # Load raw content from the given path
    #                   ) -> Optional[bytes]:
    #     return self.storage.file__content(path)


    # todo: see if we need this method (this was originally developed during one of the first architectures, but we will probably be better with an Storage_FS__Stats class (which can then take into account limitations of the current storage)
    # todo: this should return a python object (and most likely moved into a Memory_FS__Stats class)
    def stats(self) -> Dict[Safe_Id, Any]:                                                     # Get file system statistics
        total_size = 0
        for path in self.storage.files__paths():
            if path.endswith(FILE_EXTENSION__MEMORY_FS__FILE__CONFIG):                              # todo: we need a better way to only get the .config files (and calculate its size)
                fs_file = self.load(path)                                                           # todo: review the existance of this method, since this could have big performance implications
                content = fs_file.content()
                total_size += len(content)                                                          # todo: use the file size instead

        return {Safe_Id("type")            : Safe_Id("memory")               ,
                Safe_Id("file_count")      : len(self.storage.files__paths ()),
                Safe_Id("total_size")      : total_size                      }
