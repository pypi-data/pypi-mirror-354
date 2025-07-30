from typing import Optional, TypedDict
from langchain_core.messages import BaseMessage

from codefabric.types.enums import PatchType

class Requirements(TypedDict):
    project_name: str
    project_description: str
    packages: list[str]
    technology : str

class FileInfo(TypedDict):
    name: str
    path : str
    dependencies : list[str]
    technical_specifications : str
    is_generated : bool
    code : str | None

class FileInfoDebugAndFix(TypedDict):
    name: str
    path : str
    code : str | None

class ResultState(TypedDict):
    messages : list[BaseMessage]
    success : bool
    error : str | None
    version : int
    retries : int

class PatchDetails(TypedDict):
    current_file_path : str 
    file_content : Optional[str]
    move_to_file_path : Optional[str]

class Patch(TypedDict):
    patch_type : PatchType 
    patch_details : PatchDetails

class Patches(TypedDict):
    patches : list[Patch] 
    steps : list[str]