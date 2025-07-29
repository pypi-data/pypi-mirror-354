from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.file.File_FS                             import File_FS
from memory_fs.file.actions.Memory_FS__File__Paths      import Memory_FS__File__Paths
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage


class File_FS__Content(File_FS):
    file__config : Schema__Memory_FS__File__Config
    storage      : Memory_FS__Storage

    @cache_on_self                                                              # todo: add to project principles: the @cache_on_self can only be used in cases like this where we are getting the file__config value from the self.file__config , which means that it is always the same
    def file_fs__paths(self):
        return Memory_FS__File__Paths(file__config=self.file__config)

    def bytes(self):
        for path in self.file_fs__paths().paths__content():                     # todo: see if we need something like Enum__Memory_FS__File__Exists_Strategy here, since at the moment this is going to go through all files, and return when we find some data
            file_bytes = self.storage.storage_fs.file__bytes(path)              # todo: this storage.storage_fs needs to be refactored once the storage_fs is fully implemented
            if file_bytes:                                                      # todo: see if we should get this info from the metadata, or if it is ok to just load the first one we find , or if we should be following the Enum__Memory_FS__File__Exists_Strategy strategy
                return file_bytes



