from memory_fs.file.actions.File_FS__Exists             import File_FS__Exists
from memory_fs.file.actions.Memory_FS__File__Paths      import Memory_FS__File__Paths
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Memory_FS__File__Data(Type_Safe):
    file__config : Schema__Memory_FS__File__Config
    storage      : Memory_FS__Storage

    @cache_on_self
    def file_fs__exists(self):
        return File_FS__Exists(file__config=self.file__config, storage=self.storage)

    def memory_fs__paths(self):
        return Memory_FS__File__Paths(file__config=self.file__config)

    def exists(self):
        return self.file_fs__exists().config()              # if the .config() exists, then the file 'exists'

    def paths(self):
        return self.memory_fs__paths().paths()

