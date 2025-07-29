from osbot_utils.utils.Dev import pprint

from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from memory_fs.file.actions.Memory_FS__File__Paths import Memory_FS__File__Paths
from memory_fs.schemas.Schema__Memory_FS__File__Config import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage import Memory_FS__Storage
from osbot_utils.type_safe.Type_Safe                   import Type_Safe


class File_FS__Exists(Type_Safe):
    file__config: Schema__Memory_FS__File__Config
    storage     : Memory_FS__Storage

    @cache_on_self
    def file_fs__paths(self):
        return Memory_FS__File__Paths(file__config=self.file__config)

    def config(self) -> bool:
        config_paths = self.file_fs__paths().paths__config()
        return self.check_using_strategy(config_paths)

    def content(self) -> bool:
        config_paths = self.file_fs__paths().paths__content()
        return self.check_using_strategy(config_paths)

    def metadata(self) -> bool:
        raise NotImplementedError

    def check_using_strategy(self, paths):
        for path in paths:                                                          # todo: add the exists_strategy since at the moment this is implementing the Enum__Memory_FS__File__Exists_Strategy.ANY
            if self.storage.storage_fs.file__exists(path):
                return True                                                         # when Enum__Memory_FS__File__Exists_Strategy.ANY if we find at least one, return true
        return False                                                                # if none were found, return False