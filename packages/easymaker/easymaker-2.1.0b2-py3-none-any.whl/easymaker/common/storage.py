from pydantic import Field

from easymaker.common.base_model.easymaker_base_model import BaseModel


class Storage(BaseModel):
    storage_size: int = Field(validation_alias="storageSize")


class Nas(BaseModel):
    mount_dir_name: str = Field(validation_alias="mountDirName")
    nas_uri: str = Field(validation_alias="nasUri")
