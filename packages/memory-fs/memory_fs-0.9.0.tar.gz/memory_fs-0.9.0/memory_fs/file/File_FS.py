from osbot_utils.helpers.safe_str.Safe_Str__Hash import safe_str_hash

from memory_fs.file.actions.Memory_FS__File__Config     import Memory_FS__File__Config
from memory_fs.file.actions.Memory_FS__File__Create     import Memory_FS__File__Create
from memory_fs.file.actions.Memory_FS__File__Data       import Memory_FS__File__Data
from memory_fs.file.actions.Memory_FS__File__Edit       import Memory_FS__File__Edit
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Metadata import Schema__Memory_FS__File__Metadata
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from osbot_utils.type_safe.Type_Safe                    import Type_Safe



class File_FS(Type_Safe):
    file_config : Schema__Memory_FS__File__Config
    storage     : Memory_FS__Storage

    @cache_on_self
    def file__create(self):                                                                     # todo: rename these methods to file_fs__*
        return Memory_FS__File__Create(file__config=self.file_config, storage=self.storage)

    @cache_on_self
    def file__data(self):
        return Memory_FS__File__Data(file__config=self.file_config, storage= self.storage)

    @cache_on_self
    def file__edit(self):
        return Memory_FS__File__Edit(file__config=self.file_config, storage= self.storage)

    @cache_on_self
    def file_fs__content(self):
        from memory_fs.file.actions.File_FS__Content import File_FS__Content                        # todo: fix this circular import
        return File_FS__Content(file__config=self.file_config, storage= self.storage)

    # helper methods that are very common in files

    def create(self):
        return self.file__create().create__config()

    @cache_on_self
    def config(self) -> Memory_FS__File__Config:
        return Memory_FS__File__Config(file__config=self.file_config, storage= self.storage)        # todo: wrap the file__config and storage in another class since there are tons of methods that always need these two objects

    def content(self) -> bytes:
        return self.file_fs__content().bytes()

    def exists(self):
        return self.file__data().exists()

    def file_id(self):
        return self.file_config.file_id

    def metadata(self):
        content      = self.content()
        metadata = Schema__Memory_FS__File__Metadata()                                                  # todo: implement the logic to create, load and save the metadata file
        if content:
            metadata.content__hash = safe_str_hash(content.decode())                                    # todo: this should be calculated on create/edit (and saved to storage)
        return metadata